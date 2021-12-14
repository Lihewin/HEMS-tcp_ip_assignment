import sqlite3
import time
import threading


class analyser:
    power_per_sensor_data = None
    general_power_data = None
    cursor = None
    conn = None

    lock = threading.Lock()

    def __init__(self):
        self.conn = sqlite3.connect(r"HEMS.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    # 返回一个元组集合，每个元组首位为id，次位为该id传感器的当前功率
    def power_per_sensor(self):
        self.lock.acquire()
        self.cursor.execute(
            "select id,round(avg(power),3) from raw_data where time >= %d GROUP BY id" % round(time.time() - 1))
        self.power_per_sensor_data = self.cursor.fetchall()
        self.lock.release()
        return self.power_per_sensor_data

    # 返回一个元组集合，首位为power_per_sensor本身，次位为系统总功率
    def general_power(self):
        self.power_per_sensor()
        total = 0
        for each_data in self.power_per_sensor_data:
            total = total + each_data[1]
        self.lock.acquire()
        # 防止在算百分比的时候由于多线程读写的不确定性导致用来计算的总功率和更新后的总功率不同
        self.general_power_data = [self.power_per_sensor_data, total]
        self.lock.release()
        return total

    # 返回一个元组集合，格式如下：
    # [[(id, 该id瞬时功率, 该id占系统平均值),……], 总功率]
    def power_percents(self):
        if self.general_power_data is None:
            self.general_power()
        gp_data = self.general_power_data
        new_data_list = []
        for each_data in gp_data[0]:
            new_data = each_data + (round((each_data[1] / gp_data[1]) * 100, 2),)
            new_data_list.append(new_data)
        gp_data[0] = new_data_list
        return gp_data

    # 给网页端控制数据库使用
    def acquire_state_data(self, sensor_id: int):
        self.lock.acquire()
        result = self.cursor.execute(f"SELECT state FROM state_data WHERE id == {sensor_id}").fetchall()
        self.lock.release()
        if result:
            return result[0][0]
        else:
            return None

    def set_state_to(self, state: str, sensor_id: int):
        self.lock.acquire()
        self.cursor.execute(f"UPDATE state_data SET state = \"{state}\" WHERE id == {sensor_id}")
        self.conn.commit()
        self.lock.release()

    def set_all_state_to(self, state: str):
        self.lock.acquire()
        self.cursor.execute(f"UPDATE state_data SET state = \"{state}\"")
        self.conn.commit()
        self.lock.release()

    def get_all_sensor_id(self):
        self.lock.acquire()
        result = self.cursor.execute(f"SELECT id FROM state_data")
        self.lock.release()
        s_list = []
        for i in result:
            if i:
                s_list.append(i[0])
        return s_list


# for testing
if __name__ == "__main__":
    new_class = analyser()
    print(new_class)
