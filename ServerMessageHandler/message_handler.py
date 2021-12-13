import json

import threading

from ServerMessageHandler.add_raw_data import add_raw_data

next_loop_flag_mutex = threading.Lock()


# 0.这个类仅允许在Socket_server初始化时被实例化一次
# 1.当接收到的关键数据不完整时，应该关闭传感器
# 2.接收到的数据完整时，应当返回传感器心跳包
# 3.没有收到数据的时候，应当用不到这个函数


class message_handler:
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
        if not self.adder.acquire_state_data(data['id']):
            self.adder.add_state_data(data['id'], data['state'])

        # 当传感器忙时，应当向其回传off命令
        if data["state"] == "suspend":
            self.adder.add_state_data(data['id'], "off")
            return self.off_bytes

        # 当传感器不忙时，查看flag，决定下一个循环是否需要开启
        else:
            if self.adder.acquire_state_data(data['id']) == "on":
                self.adder.add_raw_data(data)
            return self.ok_bytes
