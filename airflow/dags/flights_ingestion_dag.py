import os
from datetime import datetime
import pendulum
import subprocess

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryDeleteTableOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.models import Variable

from flightradar import FlightRadar24Client
from google.cloud import storage


Variable.set("TZ", os.environ.get("TZ"))
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
STG_BIGQUERY_DATASET = os.environ.get("STG_BIGQUERY_DATASET")

# running gcloud auth activate-service-account to authorize gsutil command
CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
authenticate = subprocess.run(f"gcloud auth activate-service-account --key-file={CREDENTIALS}", shell=True, text=True)


flights_data_file = '{{ data_interval_start.in_timezone(var.value.get(\'TZ\')).strftime(\'%Y-%m-%d_%H:%M:%S\') }}.csv'
local_flights_data_file = AIRFLOW_HOME + '/{{ data_interval_start.in_timezone(var.value.get(\'TZ\')).strftime(\'%Y-%m-%d_%H:%M:%S\') }}.csv'


latitude = float(os.environ.get("LATITUDE"))
longitude = float(os.environ.get("LONGITUDE"))
radius = float(os.environ.get("RADIUS"))


def upload_to_gcs(bucket, gcs_path, src_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(src_file)


local_tz = pendulum.timezone(Variable.get("TZ"))
start = datetime(2024, 3, 10, tzinfo=local_tz)

# DAG to ingest flight data from the API every 15 minutes to a GCS bucket
ingest_flight_data_every_15_min = DAG(
    "ingest_flight_data_every_15_min",
    catchup=False,
    start_date=start,
    schedule_interval='*/15 * * * *'
)
with ingest_flight_data_every_15_min:
    
    ingest_flights_to_local_task = PythonOperator(
        task_id='ingest_flights_to_local',
        python_callable=FlightRadar24Client().getFlightsInArea,
        op_kwargs={
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
            "output": local_flights_data_file
        }
    )

    upload_to_gcs_task = PythonOperator(
        task_id='upload_flights_data_to_gcs',
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "gcs_path": f'Flights/{flights_data_file}',
            "src_file": local_flights_data_file
        }
    )

    remove_local_file_task = BashOperator(
        task_id="remove_local_file",
        bash_command=f"rm {local_flights_data_file}"
    )

    ingest_flights_to_local_task >> upload_to_gcs_task >> remove_local_file_task


# DAG to update the hourly external table in BigQuery every hour using data from the GCS bucket
update_hourly_external_table = DAG(
    "update_hourly_table",
    catchup=False,
    start_date=start,
    schedule_interval='0 * * * *'
)
with update_hourly_external_table:
    
    # delay execution of tasks to not coincide with ingest_flight_data_every_15_min DAG
    delay_bash_task = BashOperator(
        task_id="delay_bash_task",
        bash_command="sleep 5s"
    )

    # delete current hourly external table if it exists
    delete_hourly_external_table_task = BigQueryDeleteTableOperator(
        task_id="delete_hourly_bigquery_external_table_task",
        deletion_dataset_table=f"{PROJECT_ID}.{STG_BIGQUERY_DATASET}.external_table_hourly_flights",
        ignore_if_missing=True
    )
    
    # list the last 4 files from the bucket, which corresponds to the last hour of flights data: 60min/15min = 4
    get_hourly_flights_data_files = subprocess.run(f"gsutil ls gs://{BUCKET}/Flights/ | tail -n 4", shell=True, capture_output=True, text=True)
    hourly_flights_data_files = get_hourly_flights_data_files.stdout.split('\n')[:-1]
    create_hourly_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="create_hourly_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": STG_BIGQUERY_DATASET,
                "tableId": "external_table_hourly_flights",
            },
            "externalDataConfiguration": {
                "sourceFormat": "CSV",
                "sourceUris": hourly_flights_data_files,
                "autodetect": True,
            },
        },
    )

    delay_bash_task >> delete_hourly_external_table_task >> create_hourly_external_table_task


# DAG to update the daily external table in BigQuery every hour using data from the GCS bucket
update_daily_external_table = DAG(
    "update_daily_table",
    catchup=False,
    start_date=start,
    schedule_interval='0 * * * *'
)
with update_daily_external_table:
    
    # delay execution of tasks to not coincide with ingest_flight_data_every_15_min DAG and update_hourly_external_table DAG
    delay_bash_task = BashOperator(
        task_id="delay_bash_task",
        bash_command="sleep 10s"
    )
    
    # delete current daily external table if it exists
    delete_daily_external_table_task = BigQueryDeleteTableOperator(
        task_id="delete_daily_bigquery_external_table_task",
        deletion_dataset_table=f"{PROJECT_ID}.{STG_BIGQUERY_DATASET}.external_table_daily_flights",
        ignore_if_missing=True
    )
    
    # list the last 96 files from the bucket, which corresponds to the last 24 hours of flights data: (60min x 24) / 15min = 96
    get_daily_flights_data_files = subprocess.run(f"gsutil ls gs://{BUCKET}/Flights/ | tail -n 96", shell=True, capture_output=True, text=True)
    daily_flights_data_files = get_daily_flights_data_files.stdout.split('\n')[:-1]
    create_daily_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="create_daily_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": STG_BIGQUERY_DATASET,
                "tableId": "external_table_daily_flights",
            },
            "externalDataConfiguration": {
                "sourceFormat": "CSV",
                "sourceUris": daily_flights_data_files,
                "autodetect": True,
            },
        }, 
    )

    delay_bash_task >> delete_daily_external_table_task >> create_daily_external_table_task
