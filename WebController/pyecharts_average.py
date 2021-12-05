import time

import pywebio.output
from pyecharts.charts import *
from pyecharts import options as opts
from pywebio.session import run_js


def hello():
    data = [int(time.time())]
    return data


def board():
    liquid = (Liquid()
              .add(series_name='hello', data=hello(), shape='circle')
              .set_global_opts(title_opts=opts.TitleOpts('main'))
              )
    liquid.render_notebook()
    with pywebio.output.use_scope('fsd') as s:
        while True:
            pywebio.output.put_html(liquid.render_notebook())
            time.sleep(2)
            pywebio.output.clear('fsd')
