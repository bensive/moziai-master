# 时间 : 2021/09/16 17:14
# 作者 : 张志高
# 文件 : scenario_create
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment


os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, '红蓝想定.scen', etc.SIMULATE_COMPRESSION,
                  etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')
result, submarine_1 = red_side.add_submarine('潜艇1', 5, 17.6347078803726, 126.424686148705, 50)


print(124)
