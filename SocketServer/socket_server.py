import socketserver
import threading
import time

print_mutex = threading.Lock()


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data_received = self.request.recv(1024).strip()
            print_string_(data_received)
            self.request.sendall(b"{\"result\":\"ok\"}")
            time.sleep(0.01)


def print_string_(data):
    print_mutex.acquire()
    print(data)
    print_mutex.release()


def run():
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 11451), MyServer)
    server.serve_forever()
