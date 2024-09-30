from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args={
    'retries':1 ,
    'retry_delay': timedelta(minutes=1)
}

def get_data():
    import requests
    from random import random
    long = round(random(), 2)
    lat = -round(random(),2)
    res = requests.get('https://api.open-meteo.com/v1/forecast', params={'latitude': long, 'longitude':lat, "current":"temperature_2m"})
    return res

def write_kafka():
    import json
    from quixstreams import Application
    import logging
    app = Application(
        broker_address='broker-1:19092,broker-2:19092,broker-3:19092',
        loglevel='DEBUG'
    )

    with app.get_producer() as producer:
        data = get_data()
        producer.produce(
            topic='weather-data',
            key='accra',
            value=json.dumps(data.json())
        )
        logging.debug('PRODUCED! SLEEPING')

def retrieve():
    from quixstreams import Application
    import logging
    import json
    app = Application(
        broker_address='localhost:49092,localhost:39092,localhost:29092',
        loglevel='DEBUG',
        consumer_group='opp',
        auto_offset_reset='earliest'
        )
    with app.get_consumer() as consumer:
        while True:
            consumer.subscribe(['weather-data'])
            msg = consumer.poll(1)
            if msg is None:
                print('waiting...!')
            elif msg.error() is not None:
                raise Exception(msg.error())
            else:
                print(json.loads(msg.value()))

with DAG(
    'kafka_DAG',
    default_args=default_args,
    description='kafka_DAG',
    schedule_interval=timedelta(seconds=30),
    start_date=datetime(2024,1,1),
    catchup=False,
    tags=['example'],
) as dag:
    kafka_dat = PythonOperator(
        task_id="kafka_dat",
        python_callable=write_kafka,
    )
