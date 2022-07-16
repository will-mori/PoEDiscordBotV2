#DB TestFile

from site import USER_BASE
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
DB = os.getenv("MYSQL_DB")
PASSWORD = os.getenv("MYSQL_PASSWORD")


conn = mysql.connector.connect(host=HOST,database=USER,user=DB,password=PASSWORD)
print("Connected")

