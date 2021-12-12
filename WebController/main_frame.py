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

    # 创建三个图表的三个视图
    def create_pyecharts_backend_threads():
        t_general_power = threading.Thread(target=pyecharts_related.general_power.general_power_frame)
        register_thread(t_general_power)
        t_general_power.start()

        t_power_percents = threading.Thread(target=pyecharts_related.power_percents.power_percents_frame())
        register_thread(t_power_percents)
        t_power_percents.start()

        t_power_per_sensor = threading.Thread(target=pyecharts_related.power_per_sensor.power_per_sensor_frame())
        register_thread(t_power_per_sensor)
        t_power_per_sensor.start()

    create_pyecharts_backend_threads()


# 启动三个页面的后端接口和前端页面
main_app.wsgi_app = DispatcherMiddleware(main_app.wsgi_app, {
    # 饼图和条形图不需要呈现历史数据，所以使用向前端页面全量更新数据。
    '/power_percents': pyecharts_related.power_percents.power_percents,
    '/power_percents_backend': pyecharts_related.power_percents_backend.power_percents_backend,

    '/power_per_sensor': pyecharts_related.power_per_sensor.power_per_sensor,
    '/power_per_sensor_backend': pyecharts_related.power_per_sensor_backend.power_per_sensor_backend,

    # 折线图需要呈现历史数据，所以使用增量更新
    '/general_power': pyecharts_related.general_power.general_power,
    '/general_power_backend': pyecharts_related.general_power_backend.general_power_backend,
})


# 不要为难后端人写前端了
def start_main():
    main_app.add_url_rule('/', 'webio_view', webio_view(main_controller),
                          methods=['GET', 'POST', 'OPTIONS'])
    main_app.run(host="localhost", port=80, debug=True)


# 测试用
if __name__ == "__main__":
    main_app.add_url_rule('/', 'webio_view', webio_view(main_controller),
                          methods=['GET', 'POST', 'OPTIONS'])
    main_app.run(host="localhost", port=80, debug=True)
