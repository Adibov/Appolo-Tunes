# Connect to the PostgreSQL database
import os
import smtplib
import time
from email.mime.text import MIMEText

import psycopg2
import requests

from request_handler.request_status import RequestStatus

db_conn = psycopg2.connect(
    dbname="requests_db",
    user="request_manager",
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "db"),
    port="5432"
)

SPOTIFY_URL = "https://spotify23.p.rapidapi.com/recommendations/"


def _get_all_ready_requests() -> list[tuple[str, str]]:
    cursor = db_conn.cursor()
    cursor.execute("SELECT email, song_id FROM requests WHERE status = %s", (RequestStatus.READY.value,))
    requests = cursor.fetchall()
    cursor.close()
    return requests


def _get_spotify_recommended_songs(song_id: str) -> list[str]:
    querystring = {"limit": "10", "seed_tracks": song_id}

    headers = {
        "X-RapidAPI-Key": "4a81c77891mshe48ee23ebdc44aep156e58jsn16191838a831",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(SPOTIFY_URL, headers=headers, params=querystring)

    tracks = response.json().get('tracks', {})
    return [t['name'] + ': ' + t['external_urls']['spotify'] for t in tracks]


def _send_recommendations_to_user(email: str, recommendations: list[str]) -> None:
    sender = "hesamadibi80@gmail.com"
    recipients = [email]
    password = os.getenv("EMAIL_PASSWORD")
    msg = MIMEText("\n".join(recommendations))
    msg['Subject'] = "Spotify Recommendations"
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


if __name__ == '__main__':
    while True:
        ready_requests = _get_all_ready_requests()
        for email, song_id in ready_requests:
            recommended_songs = _get_spotify_recommended_songs(song_id)

        time.sleep(5)
