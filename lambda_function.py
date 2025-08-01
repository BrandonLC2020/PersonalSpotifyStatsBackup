import json
import os
from dotenv import load_dotenv

# It's good practice to load environment variables at the start
load_dotenv()

# Import your project's custom modules
from Managers.DatabaseManager import DatabaseManager
from Managers.SpotifyAPIManager import SpotifyAPIManager
from Types.MonthlyTopAlbums import MonthlyTopAlbums
from Types.MonthlyTopArtists import MonthlyTopArtists
from Types.MonthlyTopTracks import MonthlyTopTracks

def lambda_handler(event, context):
    """
    This function, triggered by AWS, fetches monthly Spotify stats and
    stores them in a MySQL database.
    """
    print("--- Starting Spotify stats backup ---")

    try:
        # 1. Initialize Managers
        # These classes handle the connections to the Spotify API and your database.
        database_manager = DatabaseManager()
        spotify_api_manager = SpotifyAPIManager()
        print("Successfully initialized Database and Spotify API managers.")

        # 2. Fetch Data from Spotify
        # Retrieves your top 50 tracks and artists from the last month.
        print("Fetching top tracks and artists from Spotify API...")
        top_tracks_obj = spotify_api_manager.get_top_tracks()
        top_artists_obj = spotify_api_manager.get_top_artists()

        if top_tracks_obj is None or top_artists_obj is None:
            # This handles cases where the Spotify API might fail.
            raise Exception("Failed to fetch data from Spotify. The API response was empty.")

        # 3. Process Data into Monthly Snapshots
        # This organizes the raw data into the monthly formats you defined.
        print("Processing data into monthly snapshots...")
        last_month_top_tracks = MonthlyTopTracks(top_tracks_obj)
        last_month_top_artists = MonthlyTopArtists(top_artists_obj)
        last_month_top_albums = MonthlyTopAlbums(top_tracks_obj)

        # 4. Insert Data into the Database
        # Commits the new snapshots to your MySQL database.
        print("Inserting data into the database...")
        database_manager.insert_top_artists_into_db(last_month_top_artists)
        database_manager.insert_top_tracks_into_db(last_month_top_tracks)
        database_manager.insert_top_albums_into_db(last_month_top_albums)

        print("--- Spotify stats backup finished successfully! ---")
        return {
            'statusCode': 200,
            'body': json.dumps('Spotify stats backup completed successfully!')
        }

    except Exception as e:
        # Captures any errors during the process for easier debugging in CloudWatch.
        print(f"An error occurred during execution: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }