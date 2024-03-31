# 🎵 Applo-Tunes 🎧

Applo-Tunes is a cloud-based music recognition and recommendation system developed as a personal project for Amirkabir University of Technology cloud computing course. The system consists of three microservices that work together to handle incoming requests, recognize songs, and provide song recommendations.

## 🎤 Microservices

1. **🎛️ Request Handler**
    - The Request Handler microservice is responsible for handling incoming requests from users.
    - It acts as the entry point for the Applo-Tunes system and manages the communication between the user and the other microservices.
    - It receives user requests, validates them, and routes them to the appropriate microservice for further processing.

2. **🎼 Song Recognition**
    - The Song Recognition microservice is responsible for identifying and recognizing songs based on the user's input.
    - It utilizes Shazam to match it against a database of known songs.
    - Once a song is recognized, it retrieves relevant information about the song, such as the title, artist, album, and genre.
    - The recognized song information is then passed to the Song Recommender system for further processing.

3. **🎶 Song Recommender**
    - The Song Recommender microservice is responsible for generating personalized song recommendations based on the recognized song.
    - It utilizes Spotify API to find similar songs.
    - Based on the recognized song and user's listening history, it generates a list of related songs that the user might enjoy.
    - The recommended songs are then send to the user via email.

## 🏗️ Architecture

Applo-Tunes follows a microservices architecture, where each microservice is designed to be independent, scalable, and loosely coupled. The microservices communicate with each other using well-defined APIs and messaging protocols.

## 🛠️ Technologies Used

- Programming Languages: Python
- Frameworks/Libraries: Flask, Psycopg2, Requests
- Databases: PostgreSQL
- Cloud Platform: Arvan Cloud
- Containerization: Docker, Docker Compose
- Messaging: RabbitMQ

## ⚙️ Setup and Deployment

Simply run the following commands to set up and deploy the Applo-Tunes system:
```bash
docker compose up -d
```

## 👥 Contributors

- [Amirhesam Adibinia](https://github.com/Adibov)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
