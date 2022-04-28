# 时间 : 2021/09/16 19:05
# 作者 : 张志高
# 文件 : general
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment


os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
                  etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()
red_side = env.scenario.get_side_by_name('红方')

contacts_dic = red_side.contacts

# 推演方条令
doctrine_red_side = red_side.get_doctrine()

# 任务条令
patrol_mission = red_side.get_missions_by_name('歼-16单机')
doctrine2 = patrol_mission.get_doctrine()

# 编组条令

# 单元条令
airs = red_side.aircrafts
air1 = [air for air in airs.values() if air.strName == '歼-16 #1'][0]
