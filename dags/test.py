from airflow import DAG
from datetime import datetime, timedelta, time
from airflow.operators.empty import EmptyOperator

default_args={
    'retries': 1 ,
    'retry_delay':timedelta(seconds=30),

}

with DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example']
) as dag:
    test = EmptyOperator(task_id='dummy')
