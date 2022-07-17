# Database loader
# This module assumes that the database has already been set up

from dbsupport import dblogin
import mysql.connector
from global_vars import CURRENCY_DICT, URL
import time
import requests
import datetime

if __name__ == "__main__":
    conn = dblogin()
    dbcursor = conn.cursor()
    currency_to_id = {}
    
    dbcursor.execute("SELECT * FROM currency")
    currency_ids = dbcursor.fetchall()
    for i in currency_ids:
        currency_to_id[i[1]] = i[0] 
    print(currency_to_id)

    queries = [ {"sell": "Exalted Orb", "buy": "Chaos Orb","limit": 200},
                {"sell": "Mirror of Kalandra", "buy": "Exalted Orb", "limit": 200},
                {"sell": "Awakener's Orb", "buy": "Exalted Orb", "limit": 200},
                {"sell": "Ancient Orb", "buy": "Exalted Orb", "limit": 200} 
                ]
    
    while True:

        vals = []

        start = datetime.datetime.now().replace(microsecond=0)
        for query in queries:
            with requests.post(URL, json=query) as resp:
                output = resp.json()
                for listing in output["offers"]:
                    del listing["seller_account"]
                    vals.append((listing["item_id"],listing["stash_id"],listing["stock"],currency_to_id[listing["buy"]],
                    currency_to_id[listing["sell"]], listing["conversion_rate"],listing["created_at"], str(start.isoformat())))

        sql = """INSERT INTO listings(item_id, stash_id, stock, buy, sell, conversion_rate, created_at, queried_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        dbcursor.executemany(sql, vals)
        conn.commit()
        print(f"Commit {len(vals)} records to db")
        time.sleep(5 * 60)
