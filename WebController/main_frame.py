import threading

from pywebio.output import *
from pywebio.platform.flask import webio_view
from pywebio.session import *
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import DataAnalyser
from WebController import switch_and_details, connector_controller, pyecharts_related

from flask import Flask

main_app = Flask(__name__, static_folder="templates")
analyser = DataAnalyser.analyser_backend


def main_controller():
    put_markdown('# HEMS控制系统')

    # 开关与每个传感器的功率信息
    t1 = threading.Thread(target=switch_and_details.board)
    register_thread(t1)
    put_markdown('## 实时状态与开关')
    t1.start()

    # 总控台
    t2 = threading.Thread(target=connector_controller.board)
    register_thread(t2)
    put_markdown('## 总控台')
    t2.start()

    put_markdown('## 实时分析')

    # 启动四个图表的增量更新后端
    def create_pyecharts_backend_threads():
        t_general_power = threading.Thread(target=pyecharts_related.general_power.general_power_frame, args=())
        register_thread(t_general_power)
        t_general_power.start()

        t_power_percents = threading.Thread(target=pyecharts_related.power_percents.power_percents_frame())
        register_thread(t_power_percents)
        t_power_percents.start()

        t_power_per_sensor = threading.Thread(target=pyecharts_related.power_per_sensor.power_per_sensor_frame())
        register_thread(t_power_per_sensor)
        t_power_per_sensor.start()

        t_all_sensor_history = threading.Thread(target=pyecharts_related.all_sensor_history.all_sensor_history_frame())
        register_thread(t_all_sensor_history)
        t_all_sensor_history.start()

    create_pyecharts_backend_threads()


dm = DispatcherMiddleware(main_app, {

    # 启动四个页面的后端接口和前端页面
    '/general_power': pyecharts_related.general_power.general_power,
    '/general_power_backend': pyecharts_related.general_power_backend.general_power_backend,
    '/power_percents': pyecharts_related.power_percents.power_percents,
    '/power_percents_backend': pyecharts_related.power_per_sensor_backend.power_per_sensor_backend,
    '/power_per_sensor': pyecharts_related.power_per_sensor.power_per_sensor,
    '/power_per_sensor_backend': pyecharts_related.power_percents_backend.power_percents_backend,
    '/all_sensor_history': pyecharts_related.all_sensor_history.all_sensor_history,
    '/all_sensor_history_backend': pyecharts_related.all_sensor_history_backend.all_sensor_history_backend
})


# 不要为难后端人写前端了
def start_main():
    main_app.add_url_rule('/', 'webio_view', webio_view(main_controller),
                          methods=['GET', 'POST', 'OPTIONS'])
    run_simple('localhost', 80, dm)


# 测试用
if __name__ == "__main__":
    main_app.add_url_rule('/', 'webio_view', webio_view(main_controller),
                          methods=['GET', 'POST', 'OPTIONS'])
    run_simple('localhost', 80, dm)
