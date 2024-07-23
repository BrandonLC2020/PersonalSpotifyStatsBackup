import pymongo
import os
from dotenv import load_dotenv
import numpy as np

from Types.MonthlyTopArtists import MonthlyTopArtists
from Types.MonthlyTopTracks import MonthlyTopTracks

load_dotenv()
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB = os.getenv('DATABASE_DB')

class DatabaseManager:
    def __init__(self):
        self.mongo_client = pymongo.MongoClient('CONNECTION URL')
        self.db = self.mongo_client['DATABASE NAME']
        self.track_collection = self.db['TRACK COL NAME']
        self.artist_collection = self.db['ARTIST COL NAME']
    
    def insert_top_tracks_into_db(self, top_tracks_of_the_month: MonthlyTopTracks):
        song_list = []
        for rank, track in top_tracks_of_the_month.top_tracks.items():
            track_artists_list = []
            for artist in track.artists:
                track_artists_list.append(artist.artist_id)
            song_list.append({
                "month" : top_tracks_of_the_month.month,
                "year" : top_tracks_of_the_month.year,
                "rank" : rank,
                "name" : track.name,
                "track_id" : track.track_id,
                "duration_ms" : track.duration, # in milliseconds
                "is_explicit" : track.is_explicit,
                "disc_number" : track.disc_number,
                "track_number" : track.track_number,
                "popularity" : track.popularity,
                "album_id" : track.album.album_id,
                "artist_ids" : track_artists_list,
                "acousticness" : track.track_features.acousticness,
                "danceability" : track.track_features.danceability,
                "energy" : track.track_features.energy,
                "instrumentalness" : track.track_features.instrumentalness,
                "liveness" : track.track_features.liveness,
                "loudness" : track.track_features.loudness,
                "speechiness" : track.track_features.speechiness,
                "tempo" : track.track_features.tempo,
                "valence" : track.track_features.valence
            })
        self.track_collection.insert_many(song_list)


    def insert_top_artists_into_db(self, top_artists_of_the_month: MonthlyTopArtists):
        artist_list = []
        for rank, artist in top_artists_of_the_month.top_artists.items():
            genres_list = []
            for genre in artist.genres:
                genres_list.append(genre)
            images_list = []
            for image in artist.images:
                images_list.append(image.url)
            unique_images_array = np.unique(np.array(images_list))
            artist_list.append({
                "month" : top_artists_of_the_month.month,
                "year" : top_artists_of_the_month.year,
                "rank" : rank,
                "name" : artist.name,
                "artist_id" : artist.artist_id,
                "popularity" : artist.popularity,
                "genres" : genres_list,
                "images" : unique_images_array.tolist()
            })
        self.artist_collection.insert_many(artist_list)