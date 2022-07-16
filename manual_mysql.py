# Manual MySql

from dbsupport import dblogin
import mysql.connector

if __name__ == "__main__":
    conn = dblogin()

    dbcursor = conn.cursor()
    while(True):
        sql = input()
        if sql == "quit":
            conn.close()
            break
        try:
            dbcursor.execute(sql)
            if "INSERT" in sql or "DROP" in sql or "UPDATE" in sql:
                conn.commit()
            elif "SELECT" in sql:
                result = dbcursor.fetchall()
                for i in result:
                    print(i)
            else:
                print(f"Executed command {sql}")
        except mysql.connector.errors.DatabaseError as e:
            print(f"Input raised error: {e}")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Input raised error: {e}")
