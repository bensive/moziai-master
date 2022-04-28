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
import math


def get_point_with_point_bearing_distance(lat, lon, bearing, distance):
    """
    一直一点求沿某一方向一段距离的点
    :param lat:纬度
    :param lon:经度
    :param bearing:朝向角
    :param distance:距离
    :return:
    """
    # pylog.info("lat:%s lon:%s bearing:%s distance:%s" % (lat, lon, bearing, distance))
    radiusEarthKilometres = 3440
    initialBearingRadians = radians(bearing)
    disRatio = distance / radiusEarthKilometres
    distRatioSine = sin(disRatio)
    distRatioCosine = cos(disRatio)
    startLatRad = radians(lat)
    startLonRad = radians(lon)
    startLatCos = cos(startLatRad)
    startLatSin = sin(startLatRad)
    endLatRads = asin((startLatSin * distRatioCosine) + (startLatCos * distRatioSine * cos(initialBearingRadians)))
    endLonRads = startLonRad + atan2(sin(initialBearingRadians) * distRatioSine * startLatCos,
                                     distRatioCosine - startLatSin * sin(endLatRads))
    my_lat = degrees(endLatRads)
    my_lon = degrees(endLonRads)
    dic = {"latitude": my_lat, "longitude": my_lon}
    return dic


def get_two_point_distance(lon1, lat1, lon2, lat2):
    """
    获得两点间的距离
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


def convert_lua_obj_to_dict(return_str):
    # 功能：将lua返回的对象，转化成python字典
    return_dict = {}
    if '\r\n' in return_str:
        return_list = return_str.split('\r\n')
    else:
        return_str = return_str.strip()[1:-1]
        return_list = return_str.split(',')
    for item in return_list:
        if '=' in item:
            item = item.strip()
            if item.endswith(','):
                item = item[:-1]
            kv = item.split('=')
            return_dict[kv[0].strip()] = kv[1].strip().replace("'", '')
    return return_dict


def plot_square(num, side, rp1, rp2):
    """
    根据对角线上的两个点经纬度，做一个正方形，并且平分成num个小正方形
    :param num: 一行（一列）小正方形的数量，行列数量都是num
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

    for i in range(num):
        k = 1
        for j in range(num):
            point = Referpoint('rp' + ':' + str(i) + ':' + str(j), rp1[0] - i * lat_inter, rp1[1] + k * lon_inter)
            # f1.name = 'rp' + str(i) + str(j)
            point = side.add_reference_point(point.name, point.lat, point.lon)
            k += 1
            point_list.append(point)
    # print(point_list)
    return point_list


def motion_dirc(point_list, rp1, rp2, rp3, rp4):
    """
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


def get_cell(num, rp1, rp2, rp_find):
    """

    :param num: 网格的维度
    :param rp1: 左上顶点1的经纬度  rp1=(lat1,lon1) lat纬度  lon经度
    :param rp2: 右下顶点2的经纬度
    :param rp_find: 要查找的坐标 rp_find=(lat,lon)
    :return: 所查坐标点所处区域的四个点的索引(左上角，右上角，右下角，左下角)
    """
    assert rp1[0] - rp2[0] > 0
    assert rp2[1] - rp1[1] > 0
    assert rp1[0] - rp_find[0] >= 0
    assert rp_find[1] - rp1[1] >= 0
    assert rp2[1] - rp_find[1] >= 0

    lat_gap = rp1[0] - rp2[0]
    lat_inter = lat_gap / num
    lon_gap = rp2[1] - rp1[1]
    lon_inter = lon_gap / num

    delta_lat = rp1[0] - rp_find[0]
    delta_lon = rp_find[1] - rp1[1]

    id_y_1 = math.floor(delta_lat / lat_inter)
    id_y_2 = math.ceil(delta_lat / lat_inter)
    id_x_1 = math.floor(delta_lon / lon_inter)
    id_x_2 = math.ceil(delta_lon / lon_inter)

    # 返回坐标点（非经纬度，左上角的点坐标为（0，0））
    point_1 = (id_y_1, id_x_1)  # （竖坐标，横坐标）
    point_2 = (id_y_1, id_x_2)
    point_3 = (id_y_2, id_x_2)
    point_4 = (id_y_2, id_x_1)

    return point_1, point_2, point_3, point_4


def convert_coordinate_to_lat_lon(num, rp1, rp2, rp_con):
    """

    :param num: 网格的维度
    :param rp1: 左上顶点1的经纬度  rp1=(lat1,lon1) lat纬度  lon经度
    :param rp2: 右下顶点2的经纬度
    :param rp_con: 要转换的坐标 rp_con=(y, x)
    :return: 须转换的坐标点的经纬度
    """
    assert rp1[0] - rp2[0] > 0
    assert rp2[1] - rp1[1] > 0

    lat_gap = rp1[0] - rp2[0]
    lat_inter = lat_gap / num
    lon_gap = rp2[1] - rp1[1]
    lon_inter = lon_gap / num

    lat = rp1[0] - lat_inter * rp_con[0]
    lon = rp1[1] + lon_inter * rp_con[1]

    return lat, lon


def get_sudoku(external_boundary, coordinate_points):
    """

    :param external_boundary: 区域外部边界
    :param coordinate_points: 单元所在区域四个坐标点[(3, 8), (3, 9), (4, 9), (4, 8)]
    :return:单元所在区域所在的九宫格 {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': []}
    """
    b_1, b_2, b_3, b_4, b_5, b_6 = [], [], [], [], [], []
    ret = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': []}
    cp = coordinate_points
    # 单元所在区域的边界在战斗区域的边界
    # list(set(a).intersection(set(b)))
    for bi, points in external_boundary.items():
        if bi is 'boundary_1':
            b_1 = list(set(points).intersection(set(cp)))
        elif bi is 'boundary_2':
            b_2 = list(set(points).intersection(set(cp)))
        elif bi is 'boundary_3':
            b_3 = list(set(points).intersection(set(cp)))
        elif bi is 'boundary_4':
            b_4 = list(set(points).intersection(set(cp)))
        elif bi is 'boundary_5':
            b_5 = list(set(points).intersection(set(cp)))
        elif bi is 'boundary_6':
            b_6 = list(set(points).intersection(set(cp)))
    if b_1:
        if external_boundary['boundary_1_2'][0] in b_1:
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            return ret, ['2', '3', '4']
        elif external_boundary['boundary_1_6'][0] in b_1:
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            ret['5'] = [(cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 1, cp[0][1] + 2), (cp[0][0] + 2, cp[0][1] + 2),
                        (cp[0][0] + 2, cp[0][1] + 1)]
            ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                        (cp[0][0] + 2, cp[0][1])]
            return ret, ['4', '5', '6']
        else:
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            ret['5'] = [(cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 1, cp[0][1] + 2), (cp[0][0] + 2, cp[0][1] + 2),
                        (cp[0][0] + 2, cp[0][1] + 1)]
            ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                        (cp[0][0] + 2, cp[0][1])]
            return ret, ['2', '3', '4', '5', '6']
    elif b_2:
        if cp == external_boundary['boundary_2_3']:
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            ret['5'] = [(cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 1, cp[0][1] + 2), (cp[0][0] + 2, cp[0][1] + 2),
                        (cp[0][0] + 2, cp[0][1] + 1)]
            ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                        (cp[0][0] + 2, cp[0][1])]
            return ret, ['2', '3', '4', '5', '6']
        else:
            ret['1'] = [(cp[0][0] - 1, cp[0][1] - 1), (cp[0][0] - 1, cp[0][1]), (cp[0][0], cp[0][1]),
                        (cp[0][0], cp[0][1] - 1)]
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                        (cp[0][0] + 1, cp[0][1] - 1)]
            return ret, ['1', '2', '3', '4', '8']
    elif b_3:
        if external_boundary['boundary_3_4'][0] in b_3:
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            return ret, ['2', '3', '4']
        else:
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            ret['5'] = [(cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 1, cp[0][1] + 2), (cp[0][0] + 2, cp[0][1] + 2),
                        (cp[0][0] + 2, cp[0][1] + 1)]
            ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                        (cp[0][0] + 2, cp[0][1])]
            return ret, ['2', '3', '4', '5', '6']
    elif b_4:
        if external_boundary['boundary_4_5'][0] in b_4:
            ret['1'] = [(cp[0][0] - 1, cp[0][1] - 1), (cp[0][0] - 1, cp[0][1]), (cp[0][0], cp[0][1]),
                        (cp[0][0], cp[0][1] - 1)]
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                        (cp[0][0] + 1, cp[0][1] - 1)]
            return ret, ['1', '2', '8']
        else:
            ret['1'] = [(cp[0][0] - 1, cp[0][1] - 1), (cp[0][0] - 1, cp[0][1]), (cp[0][0], cp[0][1]),
                        (cp[0][0], cp[0][1] - 1)]
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                        (cp[0][0], cp[0][1] + 1)]
            ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                        (cp[0][0] + 1, cp[0][1] + 1)]
            ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                        (cp[0][0] + 1, cp[0][1] - 1)]
            return ret, ['1', '2', '3', '4', '8']
    elif b_5:
        if external_boundary['boundary_5_6'][0] in b_5:
            ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                        (cp[0][0] + 2, cp[0][1])]
            ret['7'] = [(cp[0][0] + 1, cp[0][1] - 1), (cp[0][0] + 1, cp[0][1]), (cp[0][0] + 2, cp[0][1]),
                        (cp[0][0] + 2, cp[0][1] - 1)]
            ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                        (cp[0][0] + 1, cp[0][1] - 1)]
            return ret, ['6', '7', '8']
        else:
            ret['1'] = [(cp[0][0] - 1, cp[0][1] - 1), (cp[0][0] - 1, cp[0][1]), (cp[0][0], cp[0][1]),
                        (cp[0][0], cp[0][1] - 1)]
            ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                        (cp[0][0], cp[0][1])]
            ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                        (cp[0][0] + 2, cp[0][1])]
            ret['7'] = [(cp[0][0] + 1, cp[0][1] - 1), (cp[0][0] + 1, cp[0][1]), (cp[0][0] + 2, cp[0][1]),
                        (cp[0][0] + 2, cp[0][1] - 1)]
            ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                        (cp[0][0] + 1, cp[0][1] - 1)]
            return ret, ['1', '2', '6', '7', '8']
    elif b_6:
        ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                    (cp[0][0] + 1, cp[0][1] + 1)]
        ret['5'] = [(cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 1, cp[0][1] + 2), (cp[0][0] + 2, cp[0][1] + 2),
                    (cp[0][0] + 2, cp[0][1] + 1)]
        ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                    (cp[0][0] + 2, cp[0][1])]
        ret['7'] = [(cp[0][0] + 1, cp[0][1] - 1), (cp[0][0] + 1, cp[0][1]), (cp[0][0] + 2, cp[0][1]),
                    (cp[0][0] + 2, cp[0][1] - 1)]
        ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                    (cp[0][0] + 1, cp[0][1] - 1)]
        return ret, ['4', '5', '6', '7', '8']
    else:  # 不在边界
        ret['1'] = [(cp[0][0] - 1, cp[0][1] - 1), (cp[0][0] - 1, cp[0][1]), (cp[0][0], cp[0][1]),
                    (cp[0][0], cp[0][1] - 1)]
        ret['2'] = [(cp[0][0] - 1, cp[0][1]), (cp[0][0] - 1, cp[0][1] + 1), (cp[0][0], cp[0][1] + 1),
                    (cp[0][0], cp[0][1])]
        ret['3'] = [(cp[0][0] - 1, cp[0][1] + 1), (cp[0][0] - 1, cp[0][1] + 2), (cp[0][0], cp[0][1] + 2),
                    (cp[0][0], cp[0][1] + 1)]
        ret['4'] = [(cp[0][0], cp[0][1] + 1), (cp[0][0], cp[0][1] + 2), (cp[0][0] + 1, cp[0][1] + 2),
                    (cp[0][0] + 1, cp[0][1] + 1)]
        ret['5'] = [(cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 1, cp[0][1] + 2), (cp[0][0] + 2, cp[0][1] + 2),
                    (cp[0][0] + 2, cp[0][1] + 1)]
        ret['6'] = [(cp[0][0] + 1, cp[0][1]), (cp[0][0] + 1, cp[0][1] + 1), (cp[0][0] + 2, cp[0][1] + 1),
                    (cp[0][0] + 2, cp[0][1])]
        ret['7'] = [(cp[0][0] + 1, cp[0][1] - 1), (cp[0][0] + 1, cp[0][1]), (cp[0][0] + 2, cp[0][1]),
                    (cp[0][0] + 2, cp[0][1] - 1)]
        ret['8'] = [(cp[0][0], cp[0][1] - 1), (cp[0][0], cp[0][1]), (cp[0][0] + 1, cp[0][1]),
                    (cp[0][0] + 1, cp[0][1] - 1)]

        return ret, ['1', '2', '3', '4', '5', '6', '7', '8']

