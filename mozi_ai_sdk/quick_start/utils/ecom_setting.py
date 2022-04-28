
# 时间 : 2021/09/15 16:45
# 作者 : 张志高
# 文件 : ecom_action
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common


os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
                  etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()
red_side = env.scenario.get_side_by_name('红方')

# 使用条令设置
red_side_doctrine = red_side.get_doctrine()
red_side_doctrine.set_em_control_status('Radar', 'Active')
red_side_doctrine.set_em_control_status('Sonar', 'Active')
red_side_doctrine.set_em_control_status('OECM', 'Active')

# 分类选择设置
ships = red_side.get_ships()
ship_1 = [j for i, j in ships.items() if j.strName == '舰船-纯方位发射'][0]
ship_1.switch_sensor(radar='true', sonar='true', oecm='true')
ship_1.unit_obeys_emcon('false')
ship_1.set_radar_shutdown('false')
ship_1.set_sonar_shutdown('true')
ship_1.set_oecm_shutdown('true')

# 单个传感器设置
sensors = ship_1.get_sensor()
sensor = [j for i, j in sensors.items() if j.strName == 'AN/SPG-62型目标照射雷达'][0]
ship_1.unit_obeys_emcon('false')
sensor.switch('true')
