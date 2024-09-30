#!/bin/bash
set -e # Stop the script if any command fails

pip install --upgrade pip &&
    pip install psycopg2-binary &&
    pip install -r /opt/airflow/requirements.txt &&
    pip install apache-airflow-providers-amazon

# Initialize and upgrade the Airflow database
airflow db migrate
airflow db upgrade

# Start the Airflow scheduler and webserver
airflow scheduler &
exec airflow webserver
