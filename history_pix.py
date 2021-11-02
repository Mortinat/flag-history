import requests
import psycopg2
import time
import datetime
import os

conn = psycopg2.connect(
    database=os.environ.get("SQL_DATABASE", "name"),
    host=os.environ.get("SQL_HOST", "localhost"),
    port=os.environ.get("SQL_PORT", "5432"),
    user=os.environ.get("SQL_USER", "user"),
    password=os.environ.get("SQL_PASSWORD", "password"))
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS pix_history
               (hexColor text, indexInFlag int, timestamp timestamp default current_timestamp)''')
conn.commit()

print("sucess")

while(True):
    url=f"https://api-flag.fouloscopie.com/flag/after/{(datetime.datetime.utcnow()).isoformat()}"

    time.sleep(60)

    resp = requests.get(url=url)
    data = resp.json()

    ti = time.time()
    for line in data:
        cur.execute(f"INSERT INTO number_pix VALUES ({line['hexColor']},{line['indexInFlag']},{time.time()})")
    
    conn.commit()