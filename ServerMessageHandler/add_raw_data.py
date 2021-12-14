import sqlite3
import threading

adder_lock = threading.Lock()


class add_raw_data:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect("HEMS.db",
                                    check_same_thread=False)
        self.cursor = self.conn.cursor()
        # 创建数据表
        self.cursor.execute("CREATE TABLE IF NOT EXISTS raw_data"
                            "(id INTEGER, sn TEXT, type TEXT, power DOUBLE, time INTEGER)")
        # 创建状态表
        self.cursor.execute("CREATE TABLE IF NOT EXISTS state_data (id INTEGER PRIMARY KEY , state TEXT)")

    def add_raw_data(self, data):
        if "power" not in data.keys():
            data["power"] = 0

        # 向数据表中添加一条记录
        adder_lock.acquire()
        self.cursor.execute(f"INSERT INTO raw_data(id, sn, type, power, time) VALUES ({data['id']},"
                            f"\"{data['sn']}\",\"{data['type']}\",{data['power']},"
                            f"{data['time']})")
        self.conn.commit()
        adder_lock.release()

    def add_state_data(self, sensor_id: int, state: str):
        if not self.acquire_state_data(sensor_id):
            adder_lock.acquire()
            self.cursor.execute(f"INSERT INTO state_data (id, state) VALUES  ({sensor_id}, \"{state}\")")
            self.conn.commit()
            adder_lock.release()
        else:
            adder_lock.acquire()
            # 向状态表中添加一条记录
            self.cursor.execute(f"UPDATE state_data SET state = \"{state}\" WHERE id == {sensor_id}")
            self.conn.commit()
            adder_lock.release()

    def acquire_state_data(self, sensor_id: int):
        adder_lock.acquire()
        result = self.cursor.execute(f"SELECT state FROM state_data WHERE id == {sensor_id}").fetchall()
        adder_lock.release()
        if not result:
            return None
        else:
            return result[0][0]
