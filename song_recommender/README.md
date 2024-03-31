# Song Recommender Service

This service handles song recommendation requests. It is built with Python, PostgreSQL, RabbitMQ, and integrates with Spotify API.

## Setup

1. Install the required Python packages: `pip install -r requirements.txt`
2. Set the following environment variables:
    - `POSTGRES_PASSWORD`: The password for your PostgreSQL database
    - `POSTGRES_HOST`: The host of your PostgreSQL database (default is 'db')
    - `RABBITMQ_HOST`: The host of your RabbitMQ server (default is 'rabbitmq')
    - `RABBITMQ_USERNAME`: The username for your RabbitMQ server
    - `RABBITMQ_PASSWORD`: The password for your RabbitMQ server
    - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID
    - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret

## Usage

Start the service with `python main.py`.

The service listens for messages on the RabbitMQ queue. Each message should contain the ID of a song recognition request. The service will fetch the song details from the database, get recommendations from Spotify based on the song, and update the request in the database with the recommended songs.

## Note

This service is part of a larger system that includes a song upload service and a song recognition service. The song recognition service publishes messages to the RabbitMQ queue that this service listens to.