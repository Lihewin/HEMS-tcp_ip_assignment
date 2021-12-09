from random import randrange

from flask.json import jsonify
from flask import Flask
from flask_cors import CORS

from pyecharts import options as opts
from pyecharts.charts import Line

power_per_sensor_backend = Flask(__name__, static_folder="templates")
CORS(power_per_sensor_backend)


def line_base() -> Line:
    line = (
        Line()
            .add_xaxis(["{}".format(i) for i in range(10)])
            .add_yaxis(
            series_name="",
            y_axis=[randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line


@power_per_sensor_backend.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


idx = 9


@power_per_sensor_backend.route("/lineDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": randrange(50, 80)})


if __name__ == "__main__":
    power_per_sensor_backend.run(port=5000, threaded=True)
