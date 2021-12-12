import time
from datetime import datetime
from random import randrange

from flask.json import jsonify
from flask import Flask
from flask_cors import CORS

from pyecharts import options as opts
from pyecharts.charts import Line

from DataAnalyser.analyser_backend import analyser

general_power_backend = Flask(__name__, static_folder="templates")
CORS(general_power_backend)

data_analyser = analyser()


def line_base() -> Line:
    line = (
        Line()
            .add_xaxis([datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            .add_yaxis(
            series_name="系统总功率",
            y_axis=[round(data_analyser.general_power(), 2)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="系统当前总功率",
                                      subtitle="单位：瓦特"),
            xaxis_opts=opts.AxisOpts(type_="time"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line


@general_power_backend.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


@general_power_backend.route("/lineDynamicData")
def update_line_data():
    return jsonify({"name": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "value": round(data_analyser.general_power(),
                                                                                         2)})


if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    general_power_backend.run(port=5000, threaded=True)
