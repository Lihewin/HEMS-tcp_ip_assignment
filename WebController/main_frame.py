import threading

from pywebio import start_server
from pywebio.output import *
from pywebio.platform.flask import webio_view
from pywebio.session import *
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from WebController import switch_and_details, connector_controller, pyecharts_draw, pyecharts_backend

from flask import Flask

main_app = Flask(__name__, static_folder="templates")


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

    t3 = threading.Thread(target=pyecharts_draw.board)
    register_thread(t3)
    put_markdown('## 实时分析')
    t3.start()


dm = DispatcherMiddleware(main_app, {
    '/pyecharts_backend_bar': pyecharts_backend.pyecharts_backend_bar
})

if __name__ == "__main__":
    main_app.add_url_rule('/', 'webio_view', webio_view(main_controller),
                          methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
    # pyecharts_backend.pyecharts_backend_bar.run(port=5000, threaded=True)
    run_simple('localhost', 80, dm)
