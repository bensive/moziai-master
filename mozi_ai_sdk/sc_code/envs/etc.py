# 时间 ： 2020/9/8 21:30
# 作者 ： Dixit
# 文件 ： etc.py
# 项目 ： moziAIBT2
# 版权 ： 北京华戍防务技术有限公司


import os

APP_ABSPATH = os.path.dirname(__file__)

#######################
SERVER_IP = "127.0.0.1"
# SERVER_IP = "192.168.1.41"
SERVER_PORT = "6060"
PLATFORM = 'windows'
# SCENARIO_NAME = "bt_test.scen"  # 距离近，有任务
SCENARIO_NAME = "phisea-redmssn"
EVAL_SCENARIO_NAME = "菲海战事-红方有任务.scen"
# SCENARIO_NAME = "海峡风暴单机AI对抗.scen"
SIMULATE_COMPRESSION = 5
DURATION_INTERVAL = 60
SIMULATE_COMPRESSION_2 = 3
DURATION_INTERVAL_2 = 15
SYNCHRONOUS = True
#######################
# app_mode
# 1--local windows train mode
# 2--local linux train mode
# 3--remote windows evaluate mode
# 4--local windows evaluate mode
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
