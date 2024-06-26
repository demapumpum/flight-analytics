#!/bin/bash

cd ../airflow
echo -e "AIRFLOW_UID=$(id -u)" >> .env
docker-compose build
docker-compose up airflow-init
docker-compose up -d
echo "Run 'docker-compose logs --follow' to see the logs."