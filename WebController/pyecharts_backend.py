from random import randrange

from flask.json import jsonify
from flask import Flask
from flask_cors import CORS

from pyecharts import options as opts
from pyecharts.charts import Line

pyecharts_backend_bar = Flask(__name__, static_folder="templates")
CORS(pyecharts_backend_bar)


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


@pyecharts_backend_bar.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


idx = 9


@pyecharts_backend_bar.route("/lineDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": randrange(50, 80)})


if __name__ == "__main__":
    pyecharts_backend_bar.run(port=5000, threaded=True)