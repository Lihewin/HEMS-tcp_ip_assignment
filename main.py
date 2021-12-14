import time

from multiprocessing import Process
import webbrowser
import SocketClient.socket_client
import SocketServer.socket_server
import WebController

if __name__ == "__main__":
    # 就不用老师提供的传感器程序了，那个东西没法生成多样化的数据。

    sc_p = Process(target=SocketClient.socket_client.run)
    ss_p = Process(target=SocketServer.socket_server.run)
    wc_p = Process(target=WebController.main_frame.start_main)
    sc_p.start()
    ss_p.start()
    time.sleep(1)
    wc_p.start()
    time.sleep(0.5)
    webbrowser.open("localhost")
