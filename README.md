# Personal Spotify Stats Backup

This project, "Personal Spotify Stats Backup," is designed to fetch your top Spotify tracks, artists, and albums, and then store this data in a MongoDB database. It automates the process of backing up your personal listening statistics.

## Features

* **Fetches Top Data:** Retrieves your top tracks, artists, and albums from Spotify using the Spotify Web API.
* **Monthly Snapshots:** Organizes the fetched data into monthly snapshots.
* **Database Storage:** Stores the retrieved Spotify statistics in a MongoDB database for historical tracking and analysis.
* **Audio Features:** For tracks, it also fetches and stores audio features like acousticness, danceability, energy, and more.

## Setup and Installation

To set up and run this project, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd PersonalSpotifyStatsBackup-c83febc599523baad90ae224eca306bd53eddc4c
    ```

2.  **Create a Virtual Environment:**
    The project includes a script to create and activate a Python virtual environment and install dependencies.
    ```bash
    ./createVirtualEnvironment.sh
    ```
    This script creates a virtual environment named `SpotifyStatsEnv` and installs the required packages from `requirements.txt`:
    * `numpy==2.1.3`
    * `pymongo==4.10.1`
    * `python-dotenv==1.0.1`
    * `Requests==2.32.3`
    * `selenium==4.26.1`

3.  **Spotify API Application Setup:**
    * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    * Log in and create a new application.
    * Note down your `Client ID` and `Client Secret`.
    * In the application settings, add `http://localhost:3000/callback` (or your chosen `NGROK_PORT`) as a Redirect URI.

4.  **Environment Variables Configuration:**
    Create a `.env` file in the root directory of the project. This file will store your sensitive information and configuration. The `.gitignore` file ensures this file is not committed to version control.
    ```
    CLIENT_ID='your_spotify_client_id'
    CLIENT_SECRET='your_spotify_client_secret'
    REDIRECT_URI_LOCAL='http://localhost:3000/callback' # Or your ngrok redirect URI
    SPOTIFY_USERNAME='your_spotify_username'
    SPOTIFY_PASSWORD='your_spotify_password'
    DATABASE_HOST='your_mongo_db_host'
    DATABASE_CONNECTION_URL='your_mongo_db_connection_url'
    DATABASE_DB='your_mongo_db_name'
    NGROK_DOMAIN='your_ngrok_domain.ngrok-free.app' # Your ngrok domain
    NGROK_PORT='3000' # Or your chosen port
    ```
    Ensure you replace the placeholder values with your actual credentials and settings.
