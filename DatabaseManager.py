import mysql.connector
import os
from dotenv import load_dotenv

from Types.MonthlyTopArtists import MonthlyTopArtists
from Types.MonthlyTopTracks import MonthlyTopTracks

load_dotenv()
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB = os.getenv('DATABASE_DB')

class DatabaseManager:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            database=DATABASE_DB
        )
        self.mycursor = self.mydb.cursor()
    
    def insert_top_tracks_into_db(self, top_tracks_of_the_month: MonthlyTopTracks):
        val = []
        for rank, track in top_tracks_of_the_month.top_tracks:
            val.append((top_tracks_of_the_month.year, top_tracks_of_the_month.year, rank, track))

    def insert_top_artists_into_db(self, top_artists_of_the_month: MonthlyTopArtists):
        pass