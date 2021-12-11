import time

from pywebio import start_server
from pywebio.output import *
from pywebio.session import *


def board():
    put_scope('details').style('height: 40px')
    while True:
        with use_scope('details', clear=True) as details:
            set_env(output_animation=False)
            put_table(board_generator())
            time.sleep(10)


def board_generator():
    return True
