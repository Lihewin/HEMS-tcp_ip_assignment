import json

import threading

from ServerMessageHandler.add_raw_data import add_raw_data

next_loop_flag_mutex = threading.Lock()


# 0.这个类仅允许在Socket_server初始化时被实例化一次
# 1.当接收到的关键数据不完整时，应该关闭传感器
# 2.接收到的数据完整时，应当返回传感器心跳包
# 3.没有收到数据的时候，应当用不到这个函数


class message_handler:
    next_loop_flag = {}
    off_bytes = b"{\"result\":\"off\"}"
    ok_bytes = b"{\"result\":\"ok\"}"
    adder = None

    def __init__(self):
        self.adder = add_raw_data()

    def data_handler(self, data_rec):
        if type(data_rec) != bytes:
            data_rec = data_rec.decode("utf-8")
        # 传感器的返回值json
        data = json.loads(data_rec)
        # 当接收到的关键数据不完整时，应该关闭传感器
        if "state" not in data.keys() or "id" not in data.keys():
            return self.off_bytes

        # 倘若新发现一个合法的传感器，应当维护状态表，设为传感器现有状态
        if data["id"] not in self.next_loop_flag:
            next_loop_flag_mutex.acquire()
            self.next_loop_flag[data["id"]] = data["state"]
            next_loop_flag_mutex.release()

        # 当传感器忙时，应当向其回传off命令
        if data["state"] == "suspend":
            return self.off_bytes

        # 当传感器关闭时，查看flag，决定下一个循环是否需要开启
        elif data["state"] == 'off':

            if self.next_loop_flag[data["id"]] == 'on':
                self.adder.add_raw_data(data)
                return self.ok_bytes

            if self.next_loop_flag[data["id"]] == 'off':
                self.adder.add_raw_data(data)
                return self.off_bytes

        # 当传感器开启时，查看flag，决定下个循环是否需要关闭
        elif data["state"] == 'on':
            if self.next_loop_flag[data["id"]] == 'on':
                self.adder.add_raw_data(data)
                return self.ok_bytes

            if self.next_loop_flag[data["id"]] == 'off':
                self.adder.add_raw_data(data)
                return self.off_bytes
        else:
            return self.off_bytes

    # 以下函数为网页控制端编写。
    def change_next_loop(self, state: str, sensor_id: str):
        next_loop_flag_mutex.acquire()
        self.next_loop_flag[sensor_id] = state
        next_loop_flag_mutex.release()

        return True

    def read_next_loop(self, sensor_id):
        if sensor_id in self.next_loop_flag.keys():
            if self.next_loop_flag[sensor_id]:
                return self.next_loop_flag[sensor_id]
        else:
            return "unknown"
