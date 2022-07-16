# Database setup file

from dbsupport import dblogin
import mysql.connector
from global_vars import CURRENCY_DICT




if __name__ == "__main__":
    print("Starting DB setup")
    conn = dblogin()
    dbcursor = conn.cursor()
    
    try:
        dbcursor.execute("""
        CREATE TABLE currency(
            id INT AUTO_INCREMENT,
            name VARCHAR(30),
            PRIMARY KEY (id)
            )
            """)

    except mysql.connector.errors.ProgrammingError:
        print("currency table already exists")
    try:
        dbcursor.execute("""
        CREATE TABLE listings(
            item_id CHAR(64),
            stash_id CHAR(64),
            stock INT,
            buy INT,
            sell INT,
            conversion_rate FLOAT,
            created_at DATETIME,
            queried_at DATETIME,
            PRIMARY KEY (item_id, stash_id, queried_at),
            FOREIGN KEY (buy) REFERENCES CURRENCY (id),
            FOREIGN KEY (sell) REFERENCES CURRENCY (id)
            )
            """)

        sql = "INSERT INTO currency(name) VALUES (%s)"
        vals = [(i,) for i in sorted(list(CURRENCY_DICT.values()))]

        dbcursor.executemany(sql, vals)

        conn.commit()
        print("Currency inserted")
    
    except mysql.connector.errors.ProgrammingError:
        print("listings table already exists")

    
    dbcursor.execute("SHOW TABLES")
    for i in dbcursor:
        print(i)
    dbcursor.execute("SELECT * FROM currency")
    currencies = dbcursor.fetchall()
    for x in currencies:
        print(x)
    print("If a table is missing or the currency list is incomplete then bad things have happened")
    conn.close()


