from flask import Flask, send_file
from flask_cors import CORS
from pywebio.output import put_html

all_sensor_history = Flask(__name__, static_folder="templates")
CORS(all_sensor_history)


# 用来每个传感器的当前功率比，饼图
@all_sensor_history.route('/')
def render():
    return send_file('all_sensor_history_static_page.html')


# 绘制一个IFRAME，显示上面的页面。
# 不知道为什么，直接在PyWebio中绘制页面会有JS导入错误。所以曲线救国。
def all_sensor_history_frame():
    put_html('''
    <iframe src='http://localhost/all_sensor_history'
    style="border: none;width: 1000px;height: 600px;"
    scrolling="no"
    ></iframe>
    ''')
