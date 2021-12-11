import sqlite3
import time


def calc():
    conn = sqlite3.connect("..\\HEMS.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("select id,avg(power) from raw_data where time >= %d GROUP BY id" % round(time.time() - 10))
    print(cur.fetchall())


calc()
