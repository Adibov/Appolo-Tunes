import atexit
import os
from typing import IO

import boto3
import pika
import psycopg2
from flask import Flask, request
from pika.credentials import PlainCredentials

from .request_status import RequestStatus

app = Flask(__name__)

s3_client = boto3.client('s3',
                         region_name='thr',
                         endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_KEY_ID'))
bucket_name = os.getenv('AWS_BUCKET_NAME')

# Connect to the PostgreSQL database
db_conn = psycopg2.connect(
    dbname="requests_db",
    user="request_manager",
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "db"),
    port="5432"
)

# Connect to RabbitMQ server
rabbit_conn = pika.BlockingConnection(
    pika.ConnectionParameters(os.getenv('RABBITMQ_HOST', 'rabbitmq'), 5672, 'request_vhost',
                              credentials=PlainCredentials(username=os.getenv('RABBITMQ_USERNAME'),
                                                           password=os.getenv('RABBITMQ_PASSWORD'))))
channel = rabbit_conn.channel()
queue_name = 'requests'
channel.queue_declare(queue=queue_name)


@app.route('/upload-song', methods=['POST'])
def upload_song():
    email = request.form.get('email', None)
    song = request.files.get('song', None)
    if not email or not song:
        return _generate_response(400, 'Invalid request')

    request_id = save_request_in_database(email)
    if request_id == -1:
        return _generate_response(500, 'Failed to save request in the database')
    song_id = f'{email}/{request_id}'
    save_song_in_s3(song.stream, song_id)
    publish_request_to_rabbitmq(request_id)
    return _generate_response(200, f'Song uploaded successfully: {request_id}')


def save_request_in_database(email: str) -> int:
    try:
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO requests (email, status) VALUES (%s, %s) RETURNING id",
                       (email, RequestStatus.PENDING.value))
        db_conn.commit()
        return cursor.fetchone()[0]
    except Exception as e:
        print("Failed to insert new request to the database: ", e)
        return -1
    finally:
        cursor.close()


def save_song_in_s3(stream: IO[bytes], song_id: str) -> None:
    s3_client.upload_fileobj(stream, bucket_name, song_id)


def publish_request_to_rabbitmq(request_id: int):
    channel.basic_publish(exchange='', routing_key=queue_name, body=request_id.to_bytes(4, byteorder='big'))


def _generate_response(status_code: int, data: any):
    return {
        'status_code': status_code,
        'data': data
    }


def exit_handler():
    print('Committing changes to the database...')
    db_conn.commit()
    print('Closing database connection...')
    db_conn.close()
    rabbit_conn.close()
    print('RabbitMQ connection closed')


atexit.register(exit_handler)
