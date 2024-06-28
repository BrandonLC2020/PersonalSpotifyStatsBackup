import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB = os.getenv('DATABASE_DB')

mydb = mysql.connector.connect(
  host=DATABASE_HOST,
  user=DATABASE_USERNAME,
  password=DATABASE_PASSWORD,
  database=DATABASE_DB
)

mycursor = mydb.cursor()