#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : pyfile.py
# Create date : 2013-07-17 19:19
# Modified date : 2020-01-09 05:50
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from __future__ import division
from __future__ import print_function

import os
import sys
from . import pylog


def read_start_step(file_path):
    start_epoch = read_start_epoch_file(file_path)
    return int(start_epoch)


def read_start_epoch(epoch_file_path):
    start_epoch = read_start_epoch_file(epoch_file_path)
    return int(start_epoch)


def read_start_epoch_file(epoch_file_path):
    f = open(epoch_file_path, "r")
    ret = f.read()
    f.close()
    return ret


def write_start_epoch_file(epoch_file_path, cur_epoch):
    f = open(epoch_file_path, "w")
    f.write(cur_epoch)
    f.close()


def write_start_step_file(file_path, cur_step):
    write_start_epoch_file(file_path,cur_step)


def create_path(path):
    """
    创建文件路径
    :param path: 文件路径
    :return:
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def create_dir(path):
    """
    创建文件夹路径
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def write_file(con, name="default", path='./tmp_file/'):
    """
    写临时文件
    :param con: 写入文件内容
    :param name: 文件名
    :param path: 文件路径
    :return:
    """
    f = create_file(path, name)
    f.write(con)
    f.close()


def get_file_full_name(path, name):
    """
    获取文件全名
    :param path: 文件路径
    :param name: 文件名
    :return:
    """
    create_path(path)
    if path[-1] == "/":
        full_name = path + name
    else:
        full_name = path + "/" + name
    return full_name


def open_file(path, name, open_type='a'):
    """
    打开文件
    :param path: 文件路径
    :param name: 文件名
    :param open_type: 打开文件方式
    :return:
    """
    file_name = get_file_full_name(path, name)
    return open_file_with_full_name(file_name, open_type)


def create_file(path, name, open_type='w'):
    """
    创建文件
    :param path: 文件路径
    :param name: 文件名
    :param open_type: 创建文件的模式
    :return:
    """
    file_name = get_file_full_name(path, name)
    return open_file_with_full_name(file_name, open_type)


def check_is_have_file(path, name):
    """
    验证是否有文件
    :param path: 文件路径
    :param name: 文件名
    :return:
    """
    file_name = get_file_full_name(path, name)
    return os.path.exists(file_name)


def open_file_with_full_name(full_path, open_type):
    """
    使用绝对路径打开文件
    :param full_path: 文件的绝对路径
    :param open_type: 打开方式
    :return:
    """
    try:
        file_object = open(full_path, open_type)
        return file_object
    except Exception as e:
        if e.args[0] == 2:
            open(full_path, 'w')
        else:
            pylog.error(e)


def delete_dir(src):
    """
    删除文件或文件夹
    :param src: 文件或文件夹
    :return:
    """
    if os.path.isfile(src):
        try:
            os.remove(src)
        except Exception as e:
            pylog.error(e)
            return False
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_dir(itemsrc)
        try:
            os.rmdir(src)
        except Exception as e:
            pylog.error(e)
            return False
    return True
