import json
import logging
import random
import threading
import time
from socket import *

import SocketServer

sensor_nums = 10


# 传感器会和服务器定期通讯
# 传感器要求服务器回传接收到的result，并根据result判断下一步是否off关闭或ok开启


class sensor:
    status_counter = 0
    next_ret_type = "on"
    sn_length = 10

    def __init__(self, self_id):
        self.self_sn = self.generate_random_str()
        self.self_id = self_id
        with open("SocketClient\\config.json", 'r') as config:
            self.config_data = json.loads(config.read())
            config.close()
        # Read json config
        self.sensor_data_gen()

    def generate_random_str(self):

        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
        length = len(base_str) - 1
        for i in range(self.sn_length):
            import random
            random_str += base_str[random.randint(0, length)]
        return random_str

    # Generate total info for sensor
    def generate_sensor_info(self):
        data_info = {"type": "data",
                     "id": self.self_id,
                     "sn": self.self_sn,
                     "time": round(time.time())}
        if self.next_ret_type == "on":
            data_info["state"] = "on"
            data_info["power"] = (random.randint(0, 99)) * 10 + random.randint(0, 999) / 100
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            return data_info_str
        elif self.next_ret_type == "off":
            data_info["state"] = "off"
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            return data_info_str
        elif self.next_ret_type == "suspend":
            data_info["state"] = "suspend"
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            return data_info_str

    # Analyse server info and change status;
    def ret_json_load(self, data_re):

        if self.status_counter >= 4:
            self.next_ret_type = "off"
        elif self.status_counter >= 2:
            self.next_ret_type = "suspend"

        if not data_re:
            self.status_counter += 1
            return

        try:
            result = json.loads(data_re)["result"]
            if result == "ok":
                self.next_ret_type = "on"
                self.status_counter = 0
            elif result == "off":
                self.status_counter += 2
            else:
                self.status_counter += 1
        except ValueError:
            self.status_counter += 1
        except KeyError:
            self.status_counter += 1

    def sensor_data_gen(self):
        tcp_socket_client = socket(AF_INET, SOCK_STREAM)
        tcp_socket_client.connect((self.config_data["ip"], int(self.config_data["port"])))
        while True:
            try:
                tcp_socket_client.send(self.generate_sensor_info().encode('utf-8'))
                data_re = tcp_socket_client.recv(1024)
                # logging.info(data_re.decode('utf-8'))
                self.ret_json_load(data_re.decode('utf-8'))

                time.sleep(float(self.config_data["interval"]))
            except WindowsError as e:
                logging.error(e)
                break


def run():
    logging.basicConfig(level=logging.WARNING)
    logging.warning("Starting client emulator.")
    logging.warning("Client numbers: " + str(sensor_nums))
    for num in range(sensor_nums):
        t = threading.Thread(target=sensor, args=(num,))
        t.start()
