import time

from DataAnalyser.analyser_backend import analyser

from pywebio.output import *
from pywebio.session import *

analyser = analyser()


def board():
    put_scope('details')
    while True:
        with use_scope('details', clear=True) as details:
            set_env(output_animation=False)
            put_table(board_generator())
            time.sleep(3)


def board_generator():
    board_list = [['传感器ID', '传感器当前功率', '开关']]

    state_on_sensors = {}
    for each_data in analyser.power_per_sensor():
        state_on_sensors[each_data[0]] = each_data[1]
    for each_sensor in analyser.get_all_sensor_id():
        if each_sensor in state_on_sensors.keys():
            board_list.append(
                [str(each_sensor), state_on_sensors[each_sensor], put_switch_button("关", "off", each_sensor, "error")])
        else:
            board_list.append([str(each_sensor), "传感器已关闭", put_switch_button("开", "on", each_sensor, "success")])
    del each_sensor
    return board_list


# 为什么要单独把放置按钮拿出来单独做一个函数呢？这是解决python神奇回调函数问题的一个玄学办法。确实麻烦，但这可以解决问题
def put_switch_button(label: str, state: str, sensor_id: int, color: str):
    result = put_button(label, onclick=lambda: switch_state(state, sensor_id, color))
    return result


def switch_state(state: str, sensor_id: int, color: str):
    analyser.set_state_to(state, sensor_id)
    toast(str(sensor_id) + "号传感器设置为" + state, color=color)


if __name__ == "__main__":
    board()
