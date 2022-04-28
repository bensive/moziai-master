#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : geo.py
# Create date : 2019-10-21 15:40
# Modified date : 2020-04-22 04:28
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from math import radians, cos, sin, asin, sqrt, degrees, atan2, degrees
from collections import namedtuple
import numpy as np
import bisect


def get_point_with_point_bearing_distance(lat, lon, bearing, distance):
    """
    功能：已知一点求沿某一方向一段距离的点
    :param lat:纬度
    :param lon:经度
    :param bearing:朝向角，正北为0， 顺时针依次增大
    :param distance:距离, 海里
    :return:
    """
    radius_earth_kilometres = 3440
    initial_bearing_radians = radians(bearing)
    dis_ratio = distance / radius_earth_kilometres
    dist_ratio_sine = sin(dis_ratio)
    dist_ratio_cosine = cos(dis_ratio)
    start_lat_rad = radians(lat)
    start_lon_rad = radians(lon)
    start_lat_cos = cos(start_lat_rad)
    start_lat_sin = sin(start_lat_rad)
    end_lat_rads = asin((start_lat_sin * dist_ratio_cosine) +
                        (start_lat_cos * dist_ratio_sine * cos(initial_bearing_radians)))
    end_lon_rads = start_lon_rad + atan2(sin(initial_bearing_radians) * dist_ratio_sine * start_lat_cos,
                                         dist_ratio_cosine - start_lat_sin * sin(end_lat_rads))
    my_lat = degrees(end_lat_rads)
    my_lon = degrees(end_lon_rads)
    dic = {"latitude": my_lat, "longitude": my_lon}
    return dic


def get_two_point_distance(lon1, lat1, lon2, lat2):
    """
    获得两点间的距离（单位，米）
    :param lon1: 1点的经度
    :param lat1: 1点的纬度
    :param lon2: 2点的经度
    :param lat2: 2点的纬度
    :return:
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000


def get_degree(latA, lonA, latB, lonB):
    """
    获得朝向与正北方向的夹角
    :param latA: A点的纬度
    :param lonA: A点的经度
    :param latB: B点的纬度
    :param lonB: B点的经度
    :return:
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng


def plot_square(num, side, rp1, rp2):
    """
    根据对角线上的两个点经纬度，做一个矩形，并且平分成num x num个小矩形
    :param num: 一行（一列）小矩形的数量，行列数量都是num
    :param side: 推演方
    :param rp1: 左上顶点1的经纬度  rp1=(lat1,lon1) lat维度  lon经度
    :param rp2: 右下顶点2的经纬度
    :return:
    """
    Referpoint = namedtuple("Referpoint", ['name', 'lat', 'lon'])
    lat_gap = rp1[0] - rp2[0]
    lat_inter = lat_gap / num
    lon_gap = rp2[1] - rp1[1]
    lon_inter = lon_gap / num
    point_list = []

    for i in range(num + 1):
        for j in range(num + 1):
            point = Referpoint('rp' + ':' + str(i) + ':' + str(j), rp1[0] - i * lat_inter, rp1[1] + j * lon_inter)
            point = side.add_reference_point(point.name, point.lat, point.lon)
            point_list.append(point)
    return point_list


def motion_dirc(point_list, rp1, rp2, rp3, rp4):
    """
    # 具体作用不明，预放弃
    rp1, rp2, rp3, rp4 顺时针正方形的参考点
    给定4一个点的名称，我需要根据plot_square画出
    朝前：从下往上3个正方形，顺时针标记参考点名称
    朝上：下下往上3个正方形，顺时针标记参考点名称
    朝后：下往上3个正方形，顺时针标记参考点名称
    返回一个字典
    """
    point_name = []
    for i in point_list:
        point_name.append(i.strName)
    Referpoint = namedtuple("Referpoint", ['name', 'lat', 'lon'])
    rp1 = Referpoint(str(rp1), rp1[0], rp1[1])
    rp2 = Referpoint(str(rp2), rp2[0], rp2[1])
    rp3 = Referpoint(str(rp3), rp2[0], rp2[1])
    rp4 = Referpoint(str(rp4), rp2[0], rp2[1])
    rp1_num = int(rp1.name[2:])
    rp2_num = int(rp2.name[2:])
    rp3_num = int(rp3.name[2:])
    rp4_num = int(rp4.name[2:])
    rp0_num = int(rp1_num) - 11  # rp1点向左上的对角点
    rp5_num = int(rp3_num) + 11  # rp3点向右下的对角点

    forward1 = [rp4.name, rp3.name, 'rp' + str(rp3_num + 10), 'rp' + str(rp4_num + 10)]
    forward2 = [rp3.name, 'rp' + str(rp3_num + 1), 'rp' + str(rp5_num), 'rp' + str(rp3_num + 10)]
    forward3 = [rp2.name, 'rp' + str(rp2_num + 1), 'rp' + str(rp3_num + 1), rp3.name]

    middle1 = ['rp' + str(rp4_num - 1), rp4.name, 'rp' + str(rp4_num + 10), 'rp' + str(rp4_num + 9)]
    middle2 = [rp1.name, rp2.name, rp3.name, rp4.name]
    middle3 = ['rp' + str(rp2_num - 10), 'rp' + str(rp2_num - 9), 'rp' + str(rp2_num + 1), rp2.name]

    backward1 = ['rp' + str(rp1_num - 1), rp1.name, rp4.name, 'rp' + str(rp4_num - 1)]
    backward2 = ['rp' + str(rp0_num), 'rp' + str(rp0_num + 1), rp1.name, 'rp' + str(rp1_num - 1)]
    backward3 = ['rp' + str(rp0_num + 1), 'rp' + str(rp0_num + 2), rp2.name, rp1.name]

    dic1 = {1: forward1, 2: forward2, 3: forward3}
    dic2 = {1: middle1, 2: middle2, 3: middle3}
    dic3 = {1: backward1, 2: backward2, 3: backward3}

    motion_dic = {'forward': dic1, 'middle': dic2, 'backward': dic3}
    for k, v in motion_dic.items():
        for i, j in v.items():
            for index, name in enumerate(j):
                if len(name[2:]) == 1:
                    s = name[0:2] + '0' + str(name[2:])
                    del j[index]
                    j.insert(index, s)
        for i, j in v.items():
            # if any(j) not in point_name:
            if not set(point_name) > set(j):
                j = [None, None, None, None]
                v[i] = j
                motion_dic[k] = v
    return motion_dic


def get_cell_middle(num, rp1, rp2, rp_find):
    """
    功能：给出画的网格，然后给一个坐标，返回这个坐标所在表格的中心点坐标
    :param num:一行（一列）小矩形的数量，行列数量都是num，总共 num*num个小矩形
    :param rp1: 左上顶点1的经纬度  rp1=(lat1,lon1) lat纬度  lon经度
    :param rp2: 右下顶点2的经纬度
    :param rp_find:要查找的坐标 rp_find=(lat,lon)
    """
    # if rp2[0] < rp1[0]: 经纬度大小，南北纬，东西经这个要怎么考虑
    ax = np.linspace(rp2[0], rp1[0], num + 1)
    col = np.linspace(rp1[1], rp2[1], num + 1)
    id_ax = bisect.bisect(ax, rp_find[0])  # 返回rp_find坐标点纬度在维度np.array的索引
    id_col = bisect.bisect(col, rp_find[1])
    lat = ax[id_ax - 1] + (ax[id_ax] - ax[id_ax - 1]) / 2
    lon = col[id_col - 1] + (col[id_col] - col[id_col - 1]) / 2
    return lat, lon
