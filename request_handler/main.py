import os

import boto3
from flask import Flask, request

app = Flask(__name__)
s3_client = boto3.client('s3',
                         region_name='thr',
                         endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_KEY_ID'))
bucket_name = os.getenv('AWS_BUCKET_NAME')


@app.route('/upload-song', methods=['POST'])
def upload_song():
    email = request.form.get('email', None)
    song = request.files.get('song', None)
    if not email or not song:
        return _generate_response(400, 'Invalid request')

    s3_client.upload_fileobj(song.stream, bucket_name, f'{email}/{song.filename}')
    return _generate_response(200, 'Song uploaded successfully')


def _generate_response(status_code: int, data: any):
    return {
        'status_code': status_code,
        'data': data
    }
