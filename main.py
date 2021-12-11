import threading
import time

import SocketClient.socket_client
import SocketServer.socket_server
import WebController.main_frame

'''
def change_state():
    time.sleep(5)
    SocketServer.socket_server.handler.change_next_loop("off", "0")
    SocketServer.socket_server.handler.change_next_loop("off", "1")
'''

if __name__ == "__main__":
    # 就不用老师提供的传感器程序了，那个东西没法生成多样化的数据。
    # 首先启动我们的通信后端和传感器模拟器
    SocketClient.socket_client.run()
    SocketServer.socket_server.run()

    # 然后启动我们的分析程序，绘图程序和网页前端。
    # WebController.main_frame.start_main()
