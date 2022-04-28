# -*- coding:utf-8 -*-
##########################################################################################################
# File name : weapon.py
# Create date : 2020-3-10
# Modified date : 2020-3-10
# All rights reserved:北京华戍防务技术有限公司
# Author:aie
##########################################################################################################


from .weapon import CWeapon


class CUnguidedWeapon(CWeapon):
    """
    动态创建非制导武器
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
