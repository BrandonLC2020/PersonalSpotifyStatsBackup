import mysql.connector
import os
from dotenv import load_dotenv

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