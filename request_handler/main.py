import os
from typing import IO

import boto3
from flask import Flask, request
import psycopg2
import atexit

from request_handler.request_status import RequestStatus

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


atexit.register(exit_handler)
