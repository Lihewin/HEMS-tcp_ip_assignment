from random import randrange

from flask.json import jsonify
from flask import Flask
from flask_cors import CORS

from pyecharts import options as opts
from pyecharts.charts import Bar

from DataAnalyser.analyser_backend import analyser

power_per_sensor_backend = Flask(__name__, static_folder="templates")

# 解决浏览器报错禁止跨域访问的错误
CORS(power_per_sensor_backend)


def bar_base() -> Bar:
    data_analyser = analyser()
    data = data_analyser.power_per_sensor()
    ids = []
    powers = []
    for i in data:
        ids.append(i[0])
        powers.append(i[1])
    bar = (
        Bar()
            .add_xaxis(ids)
            .add_yaxis(series_name="传感器", y_axis=powers)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各传感器当前功率", subtitle="功率：瓦特"),
        )
    )
    return bar


@power_per_sensor_backend.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()




if __name__ == "__main__":
    power_per_sensor_backend.run(port=5000, threaded=True)
