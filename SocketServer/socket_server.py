import json
import socketserver
import threading
import time

from ServerMessageHandler.message_handler import message_handler

print_mutex = threading.Lock()
handler = message_handler()


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        # 创建一个消息处理类
        while True:
            data_received = self.request.recv(1024).strip()
            data2send = handler.data_handler(data_received)
            self.request.send(data2send)
            time.sleep(0.5)


def run():
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 11451), MyServer)
    server.serve_forever()
