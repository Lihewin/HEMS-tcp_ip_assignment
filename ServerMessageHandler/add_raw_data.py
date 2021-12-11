import sqlite3
import threading

adder_lock = threading.Lock()


class add_raw_data:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect("HEMS.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS raw_data"
                            "(id INTEGER, sn TEXT, type TEXT, state TEXT, power DOUBLE, time INTEGER)")

    def add_raw_data(self, data):
        if "power" not in data.keys():
            data["power"] = 0

        adder_lock.acquire()
        self.cursor.execute(f"INSERT INTO raw_data(id, sn, type, state, power, time) VALUES ({data['id']},"
                            f"\"{data['sn']}\",\"{data['type']}\",\"{data['state']}\",{data['power']},"
                            f"{data['time']})")
        self.conn.commit()
        adder_lock.release()
