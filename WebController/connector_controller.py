import time

from pywebio import start_server
from pywebio.output import *
from pywebio.session import *


def board():
    with use_scope('settings_pad') as s:
        put_buttons(['设置'], [lambda: toast('settings')])
