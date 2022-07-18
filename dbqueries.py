# Query Exploration

from re import S
from dbsupport import dblogin


if __name__ == "__main__":
    conn = dblogin()
    dbcursor = conn.cursor()

    #dbcursor.execute("SELECT * FROM currency")
    #results = dbcursor.fetchall()
    #for i in results:
    #    print(i)

    dbcursor.execute("SELECT COUNT(DISTINCT L.stash_id) FROM listings L")
    results = dbcursor.fetchall()
    print("Number of unique stashes pulled over data gathering period")
    print("-"*20)
    for i in results:
        print(i)


    dbcursor.execute("SELECT C.name, S.stashes  FROM currency C, (SELECT L.sell,\
        COUNT(DISTINCT L.stash_id) as stashes FROM listings L GROUP BY L.sell) S WHERE C.id = S.sell;")
    results = dbcursor.fetchall()
    print("Number of Unique Stashes Listing Currencies")
    print("-"*20)
    for i in results:
        print(i)
    
    dbcursor.execute("SELECT * FROM (SELECT L.stash_id, COUNT(DISTINCT L.sell) AS items FROM listings\
         L GROUP BY L.stash_id) S ORDER BY S.items DESC LIMIT 10;")
    results = dbcursor.fetchall()
    print("Stashes selling the most types of currencies")
    print("-"*20)
    for i in results:
        print(i)

    dbcursor.execute("""
    WITH t1 as (
        SELECT queried_at, conversion_rate, COUNT(*) as cnt
        FROM listings L, currency C, currency C2 
        WHERE L.sell = C.id AND C.name = 'Exalted Orb' AND 
        L.sell AND L.buy = C2.id AND C2.name = 'Chaos Orb'
        GROUP BY queried_at, conversion_rate
    ), t2 as (
        SELECT queried_at, max(cnt) as cnt
        FROM t1
        GROUP BY queried_at
    )
        SELECT *
        FROM t1 NATURAL JOIN t2
    """)
    
    results = dbcursor.fetchall()
    print("Avg Conversion rate")
    print("-"*20)
    for i in results:
        print(str(i[0]), i[1], i[2])

    dbcursor.execute("""
        SELECT queried_at, conversion_rate, COUNT(*) as cnt
        FROM listings L, currency C, currency C2 
        WHERE L.sell = C.id AND C.name = 'Exalted Orb' AND 
        L.sell AND L.buy = C2.id AND C2.name = 'Chaos Orb'
        GROUP BY queried_at, conversion_rate
        HAVING cnt > 10
        ORDER BY queried_at, cnt DESC
    """)

    results = dbcursor.fetchall()
    print("Numerous listings at rates")
    print("-"*20)    
    last_time = None
    for i in results:
        if i[0] != last_time:
            print("-"*20)
            last_time = i[0]
        print(str(i[0]), i[1], i[2])
    print("-"*20)


    dbcursor.execute("""
        WITH t1 AS (SELECT L.stash_id, L.stock as stock, MIN(L.queried_at) as time
        FROM listings L, currency C, currency C2
        WHERE L.sell = C.id AND C.name = 'Exalted Orb' AND 
        L.sell AND L.buy = C2.id AND C2.name = 'Chaos Orb'
        GROUP BY L.item_id, L.stash_id, L.stock, L.sell, L.buy, L.conversion_rate, L.created_at
        ORDER BY L.stash_id, L.created_at)
        SELECT SUM(t1.stock)
        FROM t1
        GROUP BY t1.time
        ORDER BY t1.time
    """)

    results = dbcursor.fetchall()
    print("Incoming Stock")
    print("-"*20)
    for i in results:
        print(int(i[0]))

    # TODO QUERY
    #   MAKE TIME SERIES DATA FOR rates

    conn.close()
