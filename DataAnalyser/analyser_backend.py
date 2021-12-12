import sqlite3
import time
import threading


class analyser:
    power_per_sensor_data = None
    general_power_data = None
    pss_lock = threading.Lock()
    gp_lock = threading.Lock()

    def __init__(self):
        pass

    # 返回一个元组集合，每个元组首位为id，次位为该id传感器的当前功率
    def power_per_sensor(self):
        conn = sqlite3.connect(r"C:\Users\Beijiang\PycharmProjects\TCPIP_Project\HEMS.db", check_same_thread=False)
        cur = conn.cursor()
        cur.execute("select id,round(avg(power),3) from raw_data where time >= %d GROUP BY id" % round(time.time() - 1))
        self.pss_lock.acquire()
        self.power_per_sensor_data = cur.fetchall()
        self.pss_lock.release()
        return self.power_per_sensor_data

    # 返回一个元组集合，首位为power_per_sensor本身，次位为系统总功率
    def general_power(self):
        if self.power_per_sensor_data is None:
            self.power_per_sensor()
        total = 0
        for each_data in self.power_per_sensor_data:
            total = total + each_data[1]
        self.gp_lock.acquire()
        # 防止在算百分比的时候由于多线程读写的不确定性导致用来计算的总功率和更新后的总功率不同
        self.general_power_data = [self.power_per_sensor_data, total]
        self.gp_lock.release()
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


# for testing
if __name__ == "__main__":
    new_class = analyser()
    print(new_class.power_percents())
