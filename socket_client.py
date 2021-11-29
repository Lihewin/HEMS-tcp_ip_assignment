import json
import multiprocessing
import random
import time
import logging
from socket import *

sensor_nums = 30


class sensor:
    no_respond_count = 0
    next_ret_type = 0

    def __init__(self, self_id):
        self.self_sn = self.generate_random_str()
        self.self_id = self_id
        with open("config.json", 'r') as config:
            self.config_data = json.loads(config.read())
            config.close()
        # Read json config
        self.tcp_socket_client = socket(AF_INET, SOCK_STREAM)
        # Initialize a socket connection

    @staticmethod
    def generate_random_str(random_length=10):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
        length = len(base_str) - 1
        for i in range(random_length):
            import random
            random_str += base_str[random.randint(0, length)]
        return random_str

    # Generate total info for sensor
    @staticmethod
    def generate_sensor_info(self_id, self_sn, ret_type=0):
        if ret_type == 0:
            data_info = {"type": "data",
                         "id": str(self_id),
                         "sn": self_sn,
                         "power": str(random.randint(10, 2000) + random.randint(0, 99) / 100),
                         "state": "on",
                         "time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))}
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            return data_info_str
        elif ret_type == 1:
            data_info = {"type": "data",
                         "id": str(self_id),
                         "sn": self_sn,
                         "state": "suspend",
                         "time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))}
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            return data_info_str
        else:
            data_info = {"type": "data",
                         "id": str(self_id),
                         "sn": self_sn,
                         "state": "off",
                         "time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))}
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            return data_info_str

    # Analyse server info
    def ret_json_load(self, data_re):
        if not data_re:
            self.no_respond_count += 1
            if self.no_respond_count >= 1:
                return 1

    def sensor_data_gen(self, self_id):
        while True:
            try:
                self.tcp_socket_client.connect((self.config_data["ip"], int(self.config_data["port"])))
                self.tcp_socket_client.send(self.generate_sensor_info(self_id, self.self_sn, self.next_ret_type).encode(
                    'utf-8'))
                data_re = self.tcp_socket_client.recv(1024)
                # logging.info(data_re.decode('utf-8'))
                self.ret_json_load(data_re.decode('utf-8'))
                time.sleep(int(self.config_data["interval"]))
            except WindowsError as e:
                logging.error(e)
                continue


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    logging.warning("Starting client emulator.")
    logging.warning("Client numbers: " + str(sensor_nums))
    for num in range(sensor_nums):
        p = multiprocessing.Process(target=sensor, args=(num,))
        p.start()
