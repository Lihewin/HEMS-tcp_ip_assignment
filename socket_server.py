import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        data_received = self.request.recv(1024).strip()
        print(self.client_address)
        print(data_received)


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 11451), MyServer)
    server.serve_forever()
