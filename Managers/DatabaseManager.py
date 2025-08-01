import mysql.connector
import os
from dotenv import load_dotenv
import json

from Types.MonthlyTopAlbums import MonthlyTopAlbums
from Types.MonthlyTopArtists import MonthlyTopArtists
from Types.MonthlyTopTracks import MonthlyTopTracks

load_dotenv()

class DatabaseManager:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                port=os.getenv('DB_PORT')
            )
            self.cursor = self.db.cursor()
            print("Successfully connected to MySQL database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit()

    def insert_top_tracks_into_db(self, top_tracks_of_the_month: MonthlyTopTracks):
        sql = """
        INSERT INTO tracks (month, year, standing, name, track_id, duration_ms, is_explicit,
        disc_number, track_number, popularity, album_id, artist_ids)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), popularity=VALUES(popularity);
        """
        track_list = []
        for rank, track in top_tracks_of_the_month.top_tracks.items():
            artist_ids = json.dumps([artist.artist_id for artist in track.artists])
            track_data = (
                top_tracks_of_the_month.month, top_tracks_of_the_month.year, rank,
                track.name, track.track_id, track.duration, track.is_explicit,
                track.disc_number, track.track_number, track.popularity,
                track.album.album_id, artist_ids
            )
            track_list.append(track_data)

        self.cursor.executemany(sql, track_list)
        self.db.commit()
        print(f"{self.cursor.rowcount} tracks inserted/updated.")

    def insert_top_artists_into_db(self, top_artists_of_the_month: MonthlyTopArtists):
        sql = """
        INSERT INTO artists (month, year, standing, name, artist_id, popularity, genres, images)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), popularity=VALUES(popularity);
        """
        artist_list = []
        for rank, artist in top_artists_of_the_month.top_artists.items():
            genres_list = json.dumps(artist.genres)
            images_list = json.dumps([image.url for image in artist.images])
            artist_data = (
                top_artists_of_the_month.month, top_artists_of_the_month.year, rank,
                artist.name, artist.artist_id, artist.popularity, genres_list, images_list
            )
            artist_list.append(artist_data)

        self.cursor.executemany(sql, artist_list)
        self.db.commit()
        print(f"{self.cursor.rowcount} artists inserted/updated.")

    def insert_top_albums_into_db(self, top_albums_of_the_month: MonthlyTopAlbums):
        sql = """
        INSERT INTO albums (month, year, standing, name, album_id, album_type, release_date, images, artist_ids)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name);
        """
        album_list = []
        for rank, albums in top_albums_of_the_month.top_albums.items():
            for album in albums:
                images_list = json.dumps([image.url for image in album.images])
                artist_ids = json.dumps([artist.artist_id for artist in album.artists])
                album_data = (
                    top_albums_of_the_month.month, top_albums_of_the_month.year, rank,
                    album.name, album.album_id, album.album_type, album.release_date,
                    images_list, artist_ids
                )
                album_list.append(album_data)

        self.cursor.executemany(sql, album_list)
        self.db.commit()
        print(f"{self.cursor.rowcount} albums inserted/updated.")