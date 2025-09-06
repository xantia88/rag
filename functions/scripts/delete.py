import os
import psycopg

if __name__=="__main__":

    db_user = os.getenv("DB_USER", default="admin")
    db_password = os.getenv("DB_PASSWORD", default="admin")
    db_host = os.getenv("DB_HOST", default="localhost")
    db_port = os.getenv("DB_PORT", default="5432")
    db_name = os.getenv("DB_NAME", default="postgres")
    db_collection = os.getenv("DB_COLLECTION", default="items")

    connection = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    conn = psycopg.connect(connection)
    cur = conn.cursor()
    cur.execute("delete from langchain_pg_collection where name=%s", (db_collection,))
    conn.commit()
    cur.close()
    conn.close()

    print("collection deleted:",db_collection)


    
