# Setting up Airflow in Docker

1. Navigate to airflow directory of the repo.
2. Update the .env file with the proper environment and config variables.
3. Under scripts, run `startup_airflow.sh` to let docker-compose build the image and run the container.
```bash
bash startup_airflow.sh
```
4. In VSCode, click on PORTS and forward the port 8080.
![](guides/images/airflow_1.png)
5. Login to Airflow webserver on your browser using localhost:8080 and using the credentials user: airflow and pw: airflow to check if the DAGs are properly running.

Note:
* Check the data in your BigQuery dataset flights_stg as set up in terraform. 
* Use `stop_airflow.sh` to stop the DAGs from running and stopping the container.