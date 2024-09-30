import psycopg2
from quixstreams import Application
import json



def process_streams():
    app = Application(
        broker_address='localhost:49092,localhost:39092,localhost:29092',
        loglevel='DEBUG',
        consumer_group='opp',
        auto_offset_reset='earliest'
    )

    conn = psycopg2.connect(
        "dbname=testdb user=postgres password=admin host=localhost"
    )
    cur = conn.cursor()

    with app.get_consumer() as consumer:
        consumer.subscribe(['weather-data'])
        while True:
            msg = consumer.poll(1)
            if msg is None:
                print('waiting...!')
            elif msg.error() is not None:
                raise Exception(msg.error())
            else:
                # print(msg.value())
                data=json.loads(msg.value())
                # print(data)
                if data['current'].get('temperature_2m'):
                    celcuis = round(data['current']['temperature_2m'], 2)
                else:
                    celcuis = round(data['current']['temperature'], 2)
            farenheit = round((celcuis / 9 / 5) * 32, 2)
            kelvin = round(celcuis +273.15, 2)

            print(celcuis, kelvin, farenheit)

            cur.execute(f"""
                            INSERT INTO kafka.temperature_data values({celcuis}, {farenheit}, {kelvin});
                        """)
            conn.commit()

if __name__ == '__main__':
    process_streams()

# cur.execute('create schema kafka')
# conn.commit()

# cur.execute(
#     """CREATE TABLE kafka.temperature_data(
#         celcious float,
#         kelvin float,
#         farenheit float
#     );"""
# )
# conn.commit()
# conn.close()
