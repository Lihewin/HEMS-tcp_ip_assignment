import json
import multiprocessing
import random
import time
import logging
from socket import *

sensor_nums = 30
config_data = {}


def generate_random_str(randomlength=10):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        import random
        random_str += base_str[random.randint(0, length)]
    return random_str


def sensor_data_gen(self_id):
    self_sn = generate_random_str(10)
    while True:
        with open("config.json", 'r') as config:
            config_data = json.loads(config.read())
            config.close()
        tcp_socket_client = socket(AF_INET, SOCK_STREAM)
        dest_ip = config_data["ip"]
        dest_port = int(config_data["port"])
        try:
            tcp_socket_client.connect((dest_ip, dest_port))
            data_info = {"type": "data", "id": str(self_id), "sn": self_sn,
                         "power": str(random.randint(10, 2000) + random.randint(0, 99) / 100), "state": "on",
                         "time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))}
            data_info_str = json.dumps(data_info, separators=(',', ':'))
            tcp_socket_client.send(data_info_str.encode('utf-8'))
            data_re = tcp_socket_client.recv(1024)
            logging.info(data_info)
            logging.info(data_re.decode('utf-8'))
        except ConnectionRefusedError as e:
            logging.error(e)
            continue
        time.sleep(int(config_data["interval"]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    logging.warning("Starting client emulator.")
    logging.warning("Client numbers: " + str(sensor_nums))
    for num in range(sensor_nums):
        p = multiprocessing.Process(target=sensor_data_gen, args=(num,))
        p.start()