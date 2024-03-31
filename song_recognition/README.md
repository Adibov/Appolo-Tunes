# Song Recognition Service

This service handles song recognition requests. It is built with Python, PostgreSQL, RabbitMQ, AWS S3, and integrates with Shazam and Spotify APIs.

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
   - `RAPIDAPI_KEY`: Your RapidAPI key for accessing Shazam and Spotify APIs

## Usage

Start the service with `python main.py`.

The service listens for messages on the RabbitMQ queue. Each message should contain the ID of a song upload request. The service will download the song from S3, recognize it using Shazam, find it on Spotify, and update the request in the database with the Spotify ID of the song.

## Note

This service is part of a larger system that includes a song upload service. The song upload service publishes messages to the RabbitMQ queue that this service listens to.
