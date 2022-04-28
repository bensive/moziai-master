# -*- coding:utf-8 -*-
##########################################################################################################
# File name :action.py
# Create date : 2020-4-11
# Modified date : 2020-4-11
# Author : aie
# Describe : actions' father-class
# Unit : bjhs
##########################################################################################################


class CAction:
    """
    事件动作
    """

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        self.ClassName = 'CAction'
        # 态势
        self.situation = situation
