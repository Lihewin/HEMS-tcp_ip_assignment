from pywebio.output import *
from DataAnalyser.analyser_backend import analyser

analyser = analyser()


def board():
    with use_scope('settings_pad') as s:
        put_buttons(['打开所有传感器', '关闭所有传感器'],
                    [lambda: open_all_sensor(),
                     lambda: shut_all_sensor()])


def open_all_sensor():
    analyser.set_all_state_to("on")
    toast('打开所有传感器', color='success')


def shut_all_sensor():
    analyser.set_all_state_to("off")
    toast('关闭所有传感器', color='warning')


if __name__ == "__main__":
    open_all_sensor()
