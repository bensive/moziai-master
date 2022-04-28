#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : pic.py
# Create date : 2019-10-15 20:31
# Modified date : 2020-05-06 15:14
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

import os
import numpy as np
import matplotlib.pyplot as plt
from mozi_ai_sdk.uav_anti_tank.env import etc

from mozi_utils import pyfile
from mozi_utils import pylog


def create_needed_folder():
    # 创建需要的文件夹
    pyfile.create_dir(etc.CMD_LUA)
    pyfile.create_dir(etc.PATH_CSV)
    pyfile.create_dir(etc.MODELS_PATH)


def get_start_epoch():
    # 开始的幕
    start_epoch = read_file()
    pylog.info("start epochs:%s" % start_epoch)
    return start_epoch


def get_train_step():
    # 开始的步
    start_step = read_file("%s/step.txt" % etc.OUTPUT_PATH)
    train_step = int(start_step)
    return train_step


def write_file(epochs, file_path="%s/ep.txt" % etc.OUTPUT_PATH):
    """
     打开文件
    :param epochs: 幕
    :param file_path: 文件路径
    :return:
    """
    f = open(file_path, "w")
    f.write("%s" % epochs)
    f.close()


def read_file(file_path="%s/ep.txt" % etc.OUTPUT_PATH):
    """
     打开文件
    :param file_path: 文件路径
    :return:
    """

    if not os.path.exists(file_path):
        return '0'
    f = open(file_path, "r")
    ret = f.read()
    f.close()
    if not ret:
        return '0'
    return ret


def write_final_reward(reward, epochs):
    """
    保存最后的奖赏值
    :param reward: 奖赏值
    :param epochs: 幕
    :return:
    """
    file_path = "%s/final_reward.txt" % etc.OUTPUT_PATH
    if not os.path.exists(file_path):
        f = open(file_path, "w")
    else:
        f = open(file_path, "a")
    f.write("%s,%s\n" % (epochs, reward))
    f.close()


def write_loss(step, loss_value, loss_name="loss_critic"):
    """
    保存损失
    :param step: 步
    :param loss_value:损失的值
    :param loss_name:创建损失的文档名
    :return:
    """
    pyfile.create_dir(etc.OUTPUT_PATH)
    file_path = "%s/%s.txt" % (etc.OUTPUT_PATH, loss_name)
    if not os.path.exists(file_path):
        f = open(file_path, "w")
    else:
        f = open(file_path, "a")

    f.write("%s,%s\n" % (step, loss_value))
    f.close()


def read_reward_file():
    # 读取奖励文档
    epochs_list = []
    reward_list = []
    f = open("%s/final_reward.txt" % etc.OUTPUT_PATH)
    con = f.read()
    f.close()
    con_lt = con.split("\n")
    for i in range(len(con_lt) - 1):
        lt = con_lt[i].split(',')
        epochs_list.append(int(lt[0]))
        reward_list.append(float(lt[1]))
    return epochs_list, reward_list


def read_loss_file(file_name=""):
    # 读取损失文档
    epochs_list = []
    reward_list = []
    f = open(file_name)
    con = f.read()
    f.close()
    con_lt = con.split("\n")
    for i in range(len(con_lt) - 1):
        lt = con_lt[i].split(',')
        epochs_list.append(int(lt[0]))
        reward_list.append(float(lt[1]))
    return epochs_list, reward_list


def show_reward_pic():
    # 画出奖赏值的变化图
    epoch_list, reward_list = read_reward_file()
    reward_sum = 0.0
    for i in range(len(reward_list)):
        reward_sum += reward_list[i]

    reward_mean = reward_sum / len(reward_list)
    e = np.asarray(epoch_list)
    r = np.asarray(reward_list)
    plt.figure()
    plt.plot(e, r)
    plt.xlabel('Epochs')
    plt.ylabel('Reward')
    plt.show()
    plt.close()


def show_loss_pic(loss_name="loss_critic"):
    # 画出损失值的变化图
    file_name = "%s/%s.txt" % (etc.OUTPUT_PATH, loss_name)
    step_list, loss_list = read_loss_file(file_name)
    e = np.asarray(step_list)
    r = np.asarray(loss_list)
    plt.figure()
    plt.plot(e, r)
    plt.xlabel('steps')
    plt.ylabel(loss_name)
    # 使用plt.show(),然后使用plt.close()并不会关闭图，
    # plt.show()
    plt.draw()
    plt.pause(3)
    plt.close()


def show_pic():
    # 画图
    if etc.SHOW_FIGURE:
        #show_reward_pic()
        show_loss_pic("loss_actor")
        #show_loss_pic("loss_critic")
