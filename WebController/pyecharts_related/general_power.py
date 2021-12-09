from flask import Flask, send_file
from flask_cors import CORS
from pywebio.output import put_html

general_power = Flask(__name__, static_folder="templates")
CORS(general_power)


# 用来显示一个系统总功率的页面，曲线图
@general_power.route('/')
def render():
    return send_file('general_power_static_page.html')


# 绘制一个IFRAME，显示上面的页面。
# 不知道为什么，直接在PyWebio中绘制页面会有JS导入错误。所以曲线救国。
def general_power_frame():
    put_html('''
    <iframe src='http://localhost/general_power'
    style="border: none;width: 1000px;height: 600px;"
    scrolling="no"
    ></iframe>
    ''')
