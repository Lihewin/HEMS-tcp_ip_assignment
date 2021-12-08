import json


# 0.每个handler类只应该处理单个传感器的数据，处理新数据应当new一个handler类
# 1.当接收到的关键数据不完整时，应该关闭传感器
# 2.接收到的数据完整时，应当返回传感器心跳包
# 3.没有收到数据的时候，应当用不到这个函数


class message_handler:
    next_loop_flag = "on"

    def __init__(self):
        pass

    def data_handler(self, data_rec):
        if type(data_rec) != bytes:
            data_rec = data_rec.decode("utf-8")
        # 传感器的返回值json
        data = json.loads(data_rec)

        # 当接收到的关键数据不完整时，应该关闭传感器
        if "state" not in data.keys() or "id" not in data.keys():
            return b"{\"result\":\"off\"}"

        # 当传感器忙时，应当向其回传off命令
        if data["state"] == "suspend":
            return b"{\"result\":\"off\"}"

        # 当传感器关闭时，查看flag，决定下一个循环是否需要开启
        elif data["state"] == "off":
            if self.next_loop_flag == "on":
                return b"{\"result\":\"ok\"}"
            if self.next_loop_flag == "off":
                return b"{\"result\":\"off\"}"

        # 当传感器开启时，查看flag，决定下个循环是否需要关闭
        elif data["state"] == "on":
            if self.next_loop_flag == "on":
                return b"{\"result\":\"ok\"}"
            if self.next_loop_flag == "off":
                return b"{\"result\":\"off\"}"

        else:
            return b"{\"result\":\"off\"}"
