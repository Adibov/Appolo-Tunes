# Song Upload Service

This service handles song upload requests. It is built with Python, Flask, PostgreSQL, RabbitMQ, and AWS S3.

## Setup

1. Install the required Python packages: `pip install -r requirements.txt`
2. Set the following environment variables:
    - `AWS_ACCESS_KEY_ID`: Your AWS access key ID
    - `AWS_SECRET_KEY_ID`: Your AWS secret key ID
    - `AWS_BUCKET_NAME`: The name of your S3 bucket
    - `POSTGRES_PASSWORD`: The password for your PostgreSQL database
    - `POSTGRES_HOST`: The host of your PostgreSQL database (default is 'db')
    - `RABBITMQ_HOST`: The host of your RabbitMQ server (default is 'rabbitmq')
    - `RABBITMQ_USERNAME`: The username for your RabbitMQ server
    - `RABBITMQ_PASSWORD`: The password for your RabbitMQ server

## Usage

Start the service with `python main.py`.

To upload a song, send a POST request to `/upload-song` with the following form data:
- `email`: The email address associated with the request
- `song`: The song file to upload

The service will respond with a status code and a message. If the upload is successful, the message will include the ID of the request.