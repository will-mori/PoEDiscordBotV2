# Query Exploration

from re import S
from dbsupport import dblogin


if __name__ == "__main__":
    conn = dblogin()
    dbcursor = conn.cursor()

    dbcursor.execute("SELECT * FROM currency")
    results = dbcursor.fetchall()
    for i in results:
        print(i)

    dbcursor.execute("SELECT COUNT(DISTINCT L.stash_id) FROM listings L")
    results = dbcursor.fetchall()
    print("Number of unique stashes pulled over data gathering period")
    for i in results:
        print(i)


    dbcursor.execute("SELECT C.name, S.stashes  FROM currency C, (SELECT L.sell,\
        COUNT(DISTINCT L.stash_id) as stashes FROM listings L GROUP BY L.sell) S WHERE C.id = S.sell;")
    results = dbcursor.fetchall()
    print("Number of Unique Stashes Listing Currencies")
    for i in results:
        print(i)
    
    dbcursor.execute("SELECT * FROM (SELECT L.stash_id, COUNT(DISTINCT L.sell) AS items FROM listings\
         L GROUP BY L.stash_id) S ORDER BY S.items DESC LIMIT 10;")
    results = dbcursor.fetchall()
    print("Stashes selling the most types of currencies")
    for i in results:
        print(i)

    conn.close()