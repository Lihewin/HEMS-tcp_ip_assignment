import time

from pywebio import start_server
from pywebio.output import *
from pywebio.session import *


def board():
    put_scope('details').style('background-color: red; font-size: 20px; height: 40px')
    while True:
        with use_scope('details', clear=True) as details:
            set_env(output_animation=False)
            put_text(time.time())
            time.sleep(0.5)
