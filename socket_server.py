import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data_received = self.request.recv(1024).strip()
            print(self.client_address[0])
            print(data_received)
            if not data_received:
                break
            self.request.sendall(b"{\"result\":\"ok\"}")


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 11451), MyServer)
    server.serve_forever()
