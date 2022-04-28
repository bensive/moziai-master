#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : etc.py
# Create date : 2020-01-07 03:28
# Modified date : 2020-05-07 20:18
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################


import torch
import os

app_abspath = os.path.dirname(__file__)
app_abspath = os.path.dirname(app_abspath)
USE_CUDA = False
device = torch.device("cuda" if USE_CUDA else "cpu")


#######################
SERVER_IP = "127.0.0.1"
SERVER_PORT = "6060"
SERVER_PLAT = "windows"                 # windows linux
SCENARIO_NAME = "heli_anti_sub.scen"    # 直升机反潜想定
SIMULATE_COMPRESSION = 4                #推演档位
SYNCHRONOUS = True  # True同步, False异步

target_radius = 50000.0
target_name = "PL-636.3“阿尔罗萨级”柴电潜艇"

task_end_point = {"latitude": 43.4874, "longitude": 34.1755}
TRANS_DATA = True
control_noise = True
#######################
# app_mode:
# 1--local windows 本地windows模式
# 2--linux mode    linux模式
# 3--evaluate mode 比赛模式
app_mode = 1
#######################
MAX_EPISODES = 5000  # 一共训练多少轮
MAX_BUFFER = 10000
MAX_STEPS = 30  # 一共做多少次决策
DURATION_INTERVAL = 10  # 仿真时间多长做一次决策。（单位：秒）如果为1，会导致一直在转向
#######################

#######################
TMP_PATH = "%s/%s/tmp" % (app_abspath, SCENARIO_NAME)
OUTPUT_PATH = "%s/output" % app_abspath  # 多了一层目录

MODELS_PATH = "%s/Models/" % OUTPUT_PATH  # 模型输出路径
#######################
