import socketserver
import time


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data_received = self.request.recv(1024).strip()
            self.request.sendall(b"{\"result\":\"ok\"}")
            time.sleep(0.1)


def run():
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 11451), MyServer)
    server.serve_forever()
