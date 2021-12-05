import threading

from pywebio import start_server
from pywebio.output import *
from pywebio.session import *

from WebController import switch_and_details, connector_controller, pyecharts_average


def main_controller():
    put_markdown('# HEMS控制系统')

    t1 = threading.Thread(target=switch_and_details.board)
    register_thread(t1)
    put_markdown('## 实时状态与开关')
    t1.start()

    t2 = threading.Thread(target=connector_controller.board)
    register_thread(t2)
    put_markdown('## 控制面板')
    t2.start()

    t3 = threading.Thread(target=pyecharts_average.board)
    register_thread(t3)
    put_markdown('## 实时分析')
    t3.start()


if __name__ == "__main__":
    start_server(main_controller,
                 auto_open_webbrowser=True,
                 debug=True
                 )
