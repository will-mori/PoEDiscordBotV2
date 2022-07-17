#DB TestFile

import mysql.connector
from dotenv import load_dotenv
import os

def dbcreate(db_name: str):
    """
    Creates a database with the given name.  This function does not do error checking.
    The connection is closed after creating the database
    :param db_name: String name of database to be created
    :returns: None
    """
    load_dotenv()
    HOST = os.getenv("MYSQL_HOST")
    USER = os.getenv("MYSQL_USER")
    PASSWORD = os.getenv("MYSQL_PASSWORD")
    conn = mysql.connector.connect(host=HOST,user=USER,password=PASSWORD)
    dbcursor = conn.cursor()
    dbcursor.execute(f"CREATE DATABASE {db_name}")
    conn.close()



def dblogin():
    """
    Creates a connection to a database.  This function does not do error checking.
    This function relies on a value for MYSQL_DB to be define in .env
    :returns: mysql connection
    """
    load_dotenv()
    HOST = os.getenv("MYSQL_HOST")
    USER = os.getenv("MYSQL_USER")
    DB = os.getenv("MYSQL_DB")
    PASSWORD = os.getenv("MYSQL_PASSWORD")


    conn = mysql.connector.connect(host=HOST,database=DB,user=USER,password=PASSWORD)
    print("Connected to databse")
    return conn

def dbtableprint():
    """
    Prints the tables in the database.  This function does not do error checking.
    This function relies on a value for MYSQL_DB to be define in .env
    :returns: None
    """
    load_dotenv()
    HOST = os.getenv("MYSQL_HOST")
    USER = os.getenv("MYSQL_USER")
    DB = os.getenv("MYSQL_DB")
    PASSWORD = os.getenv("MYSQL_PASSWORD")


    conn = mysql.connector.connect(host=HOST,database=DB,user=USER,password=PASSWORD)
    dbcursor = conn.cursor()
    dbcursor.execute("SHOW TABLES")
    for x in dbcursor:
        print(x)
    conn.close()

if __name__ == "__main__":
    print("Testing connection to dotenv db")
    conn = dblogin()
    print("Connection made")
    conn.close()
