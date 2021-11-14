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
               (hexColor text, indexInFlag int, author text, timestamp timestamp default current_timestamp)''')
conn.commit()

cur.execute('SELECT timestamp FROM pix_history ORDER BY timestamp DESC NULLS LAST LIMIT  1;')

last_timestamp = cur.fetchall()[0][0].isoformat()

while(True):
    url=f"https://api-flag.fouloscopie.com/flag/after/{last_timestamp}"

    time.sleep(60)

    resp = requests.get(url=url)
    data = resp.json()

    last_timestamp = (datetime.datetime.utcnow()).isoformat()

    for line in data:
        cur.execute(f"INSERT INTO pix_history VALUES (%s, %s, %s)", (line['hexColor'], line['indexInFlag'], line['author']))
    
    conn.commit()