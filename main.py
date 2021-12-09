import threading
import time

import SocketClient.socket_client
import SocketServer.socket_server


def change_state():
    time.sleep(5)
    SocketServer.socket_server.handler.change_next_loop("off", "0")
    SocketServer.socket_server.handler.change_next_loop("off", "1")


if __name__ == "__main__":
    # threading.Thread(target=change_state).start()
    SocketClient.socket_client.run()
    SocketServer.socket_server.run()
