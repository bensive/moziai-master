# 时间 ： 2020/7/20 17:13
# 作者 ： Dixit
# 文件 ： etc.py
# 项目 ： moziAIBT
# 版权 ： 北京华戍防务技术有限公司

import os

APP_ABSPATH = os.path.dirname(__file__)

#######################
SERVER_IP = "127.0.0.1"
SERVER_PORT = "6060"
PLATFORM = 'windows'
# SCENARIO_NAME = "bt_test.scen"  # 距离近，有任务
# SCENARIO_NAME = "海峡风暴-资格选拔赛.scen"  # 没有任务
SCENARIO_NAME = "海峡风暴-资格选拔赛-蓝方任务随机方案-给周国进测试.scen"
# SCENARIO_NAME = "hxfb-multitask"
# SCENARIO_NAME = "海峡风暴-最新 - 护航.scen"
SIMULATE_COMPRESSION = 3
DURATION_INTERVAL = 15
SYNCHRONOUS = True
#######################
MAX_EPISODES = 5000
MAX_BUFFER = 1000000
MAX_STEPS = 30
#######################
# app_mode:
# 1--local windows 本地windows模式
# 2--linux mode    linux模式
# 3--evaluate mode 比赛模式
APP_MODE = 1
