import mysql.connector

mydb = mysql.connector.connect(
  host="brandon@100.64.138.178",
  user="brandon",
  password="MyServer22!",
  database="mydatabase"
)

mycursor = mydb.cursor()