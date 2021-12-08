import json
import socketserver
import threading
import time

from ServerMessageHandler.message_handler import message_handler

print_mutex = threading.Lock()


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        # 创建一个消息处理类
        handler = message_handler()
        while True:
            data_received = self.request.recv(1024).strip()
            print(data_received)
            data2send = handler.data_handler(data_received)
            print(data2send)
            self.request.send(data2send)
            time.sleep(0.01)


def run():
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 11451), MyServer)
    server.serve_forever()
