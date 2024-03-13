import base64
import os
import sys

import boto3
import pika
import psycopg2
import requests
from pika import PlainCredentials

from request_handler.request_status import RequestStatus

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

rabbit_conn = pika.BlockingConnection(
    pika.ConnectionParameters(os.getenv('RABBITMQ_HOST', 'rabbitmq'), 5672, 'request_vhost',
                              credentials=PlainCredentials(username=os.getenv('RABBITMQ_USERNAME'),
                                                           password=os.getenv('RABBITMQ_PASSWORD'))))
channel = rabbit_conn.channel()
queue_name = 'requests'
channel.queue_declare(queue=queue_name)

SHAZAM_URL = "https://shazam-api-free.p.rapidapi.com/shazam/recognize/"
SPOTIFY_URL = "https://spotify23.p.rapidapi.com/search/"


def handle_message(ch, method, properties, body):
    request_id = int.from_bytes(body, byteorder='big')
    print(f" [x] Received {request_id}")
    song_id = _get_song_id_from_request_id(request_id)
    song = _download_song_from_s3(song_id)
    song_name = _get_song_name_from_shazam(song)
    spotify_id = _get_spotify_id_from_song_name(song_name)
    _update_song_id_in_db(request_id, spotify_id)
    print(f" [x] Updated {request_id} song id to {spotify_id}")


def _get_song_id_from_request_id(request_id: int) -> str:
    cursor = db_conn.cursor()
    cursor.execute("SELECT email FROM requests WHERE id = %s", (request_id,))
    email = cursor.fetchone()[0]
    cursor.close()
    return f'{email}/{request_id}'


def _download_song_from_s3(song_id: str) -> bytes:
    print(f'Downloading song {song_id} from S3...')
    obj = s3_client.get_object(Bucket=bucket_name, Key=song_id)
    print(f'Downloaded song {song_id} from S3.')
    return obj['Body'].read()


def _get_song_name_from_shazam(song: bytes) -> str:
    with open('song.mp3', 'wb') as file:
        file.write(song)
    files = {"upload_file": open('song.mp3', 'rb')}
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": "shazam-api-free.p.rapidapi.com",
    }

    print('Sending request to Shazam...')
    response = requests.post(SHAZAM_URL, files=files, headers=headers)
    print('Got response from Shazam.')
    os.remove('song.mp3')
    return response.json().get('track', {}).get('title', 'Unknown')


def _get_spotify_id_from_song_name(song_name: str) -> str:
    querystring = {
        "q": song_name,
        "type": "tracks",
        "offset": "0",
        "limit": "1",
        "numberOfTopResults": "1"
    }

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    print('Sending request to Spotify...')
    response = requests.get(SPOTIFY_URL, headers=headers, params=querystring)
    print('Got response from Spotify.')
    return response.json().get('tracks', {}).get('items', [{}])[0].get('data', {}).get('id', 'Unknown')


def _update_song_id_in_db(request_id: int, song_id: str):
    cursor = db_conn.cursor()
    cursor.execute("UPDATE requests SET song_id = %s, status = %s WHERE id = %s",
                   (song_id, RequestStatus.READY.value, request_id))
    db_conn.commit()
    cursor.close()


if __name__ == '__main__':
    try:
        channel.basic_consume(queue=queue_name,
                              auto_ack=True,
                              on_message_callback=handle_message)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
