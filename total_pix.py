import requests
import psycopg2
import time
import os

conn = psycopg2.connect(
    database=os.environ.get("SQL_DATABASE", "name"),
    host=os.environ.get("SQL_HOST", "localhost"),
    port=os.environ.get("SQL_PORT", "5432"),
    user=os.environ.get("SQL_USER", "user"),
    password=os.environ.get("SQL_PASSWORD", "password"))

cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS number_pix
               (total int, timestamp timestamp default current_timestamp)''')
conn.commit()

while(True):
    time.sleep(60)
    resp = requests.get(url="https://api-flag.fouloscopie.com/flag")
    data = resp.json()

    cur.execute(f"INSERT INTO number_pix VALUES ({len(data)})")

    conn.commit()