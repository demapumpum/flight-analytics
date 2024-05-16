import os
import json
from airflow.exceptions import AirflowFailException

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
schema_file = AIRFLOW_HOME + '/scripts/schema.json'
    
def load_json(filepath):
    """
    load reference json schema
    """
    with open(filepath, 'r') as f:
        ref_schema = json.load(f)
    
    return ref_schema


def checkSchema(schema):
    """
    Check if schema of ingested data matches reference schema 
    """
    ref_schema = load_json(schema_file)

    if schema != ref_schema:
        raise AirflowFailException("Schema change detected!")