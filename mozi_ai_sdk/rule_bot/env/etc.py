# 时间 ： 2020/9/8 21:30
# 作者 ： Dixit
# 文件 ： etc.py
# 项目 ： moziAI
# 版权 ： 北京华戍防务技术有限公司


import os
import sys

APP_ABSPATH = os.path.dirname(__file__)

#######################
SERVER_IP = "127.0.0.1"
SERVER_PORT = "6060"
PLATFORM = 'windows' if sys.platform == 'win32' else sys.platform
SCENARIO_NAME = "rule_bot.scen"
SIMULATE_COMPRESSION = 3
DURATION_INTERVAL = 5
SYNCHRONOUS = True
#######################
# app_mode:
# 1--local windows 本地windows模式
# 2--linux mode    linux模式
# 3--evaluate mode 比赛模式
app_mode = 1
#######################
MAX_EPISODES = 5000
MAX_BUFFER = 1000000
MAX_STEPS = 30
#######################

#######################
TMP_PATH = "%s/%s/tmp" % (APP_ABSPATH, SCENARIO_NAME)
OUTPUT_PATH = "%s/%s/output" % (APP_ABSPATH, SCENARIO_NAME)

CMD_LUA = "%s/cmd_lua" % TMP_PATH
PATH_CSV = "%s/path_csv" % OUTPUT_PATH
MODELS_PATH = "%s/Models/" % OUTPUT_PATH
EPOCH_FILE = "%s/epochs.txt" % OUTPUT_PATH
#######################

TRANS_DATA = True
