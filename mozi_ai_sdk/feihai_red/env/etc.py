# 时间 : 2021/09/14 14:10
# 作者 : 张志高
# 文件 : etc
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

SERVER_IP = "127.0.0.1"
SERVER_PORT = "6060"
# 平台
PLATFORM = 'windows'
SCENARIO_NAME = "菲海战事-仅蓝方有任务-v2.scen"
# SCENARIO_NAME = "菲海战事-双方均无任务-v2.scen"
# 推演档位 0-1倍速，1-2倍速，2-5倍速，3-15倍速，
# 4-30倍速，5-60倍速，6-300倍速，7-900倍速，8-1800倍速
SIMULATE_COMPRESSION = 3
# 决策步长，单位秒
DURATION_INTERVAL = 30
# 推进模式: True为同步模式，False为异步模式
SYNCHRONOUS = True
# APP_MODE:
# 1 -- 本地windows模式
# 2 -- linux模式
# 3 -- 比赛模式
APP_MODE = 1
# Windows下墨子安装目录下bin目录
MOZI_PATH = 'D:/202102-mozi/Mozi/MoziServer/bin'

SCENARIO_START_TIME = 0
