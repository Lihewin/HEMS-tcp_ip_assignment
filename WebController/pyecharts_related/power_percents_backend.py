from random import randrange

from flask.json import jsonify
from flask import Flask
from flask_cors import CORS

from pyecharts import options as opts
from pyecharts.charts import Line, Pie

from DataAnalyser.analyser_backend import analyser

power_percents_backend = Flask(__name__, static_folder="templates")
CORS(power_percents_backend)


def pie_base() -> Line:
    data_analyser = analyser()
    data = data_analyser.power_per_sensor()
    pie = (
        Pie()
            .add('传感器', data, radius=[80, 150],
                 label_opts=opts.LabelOpts(formatter="传感器{b}:{d}%"))
            .set_global_opts(title_opts=opts.TitleOpts(title="传感器功率占比",
                                                       subtitle="以百分比计算",
                                                       ),

                             )
    )
    return pie


@power_percents_backend.route("/pieChart")
def get_pie_chart():
    c = pie_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    power_percents_backend.run(port=5000, threaded=True)
