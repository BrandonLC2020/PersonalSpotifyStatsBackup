import mysql.connector
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

mycursor = mydb.cursor()