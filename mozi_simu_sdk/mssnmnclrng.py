#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :mssnmnclrng.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .mission import CMission


class CMineClearingMission(CMission):
    """
    扫雷任务
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
