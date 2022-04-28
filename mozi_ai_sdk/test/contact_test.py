
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestContact(TestFramework):
    """测试探测目标"""

    def test_get_type_description(self):
        """获取探测目标的类型描述"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        info = contact.get_type_description()
        self.env.step()
        self.assertEqual(info, 'Air')

    def test_get_contact_info(self):
        """获取目标信息字典"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        info = contact.get_contact_info()
        self.env.step()
        self.assertEqual(info.get('name'), contact.strName)

    def test_get_actual_unit(self):
        """获取目标真实单元"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        info = contact.get_actual_unit()
        self.env.step()
        self.assertEqual(info.strName, '敌机1')

    def test_get_original_detector_side(self):
        """获取探测到单元的方"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        info = contact.get_original_detector_side()
        self.env.step()
        self.assertEqual(info.strName, '红方')

    def test_get_original_target_side(self):
        """获取目标单元所在方"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        info = contact.get_original_target_side()
        self.env.step()
        self.assertEqual(info.strName, '蓝方')

    def test_set_mark_contact(self):
        """标识目标立场"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        # 'F'：友方，'N'：中立，'U'：非友方，'H'：敌方
        contact.set_mark_contact('F')
        self.env.step()
        self.assertEqual(self.get_side_posture_dict(contact.m_SidePostureStanceDictionary)[self.red_side.strGuid], 1)
        contact.set_mark_contact('N')
        self.env.step()
        self.assertEqual(self.get_side_posture_dict(contact.m_SidePostureStanceDictionary)[self.red_side.strGuid], 0)
        contact.set_mark_contact('U')
        self.env.step()
        self.assertEqual(self.get_side_posture_dict(contact.m_SidePostureStanceDictionary)[self.red_side.strGuid], 2)
        contact.set_mark_contact('H')
        self.env.step()
        self.assertEqual(self.get_side_posture_dict(contact.m_SidePostureStanceDictionary)[self.red_side.strGuid], 3)

    @staticmethod
    def get_side_posture_dict(side_posture_stance_dictionary):
        dict1 = {}
        if side_posture_stance_dictionary:
            str_list = side_posture_stance_dictionary.split('@')
            for item in str_list:
                if item:
                    item_list = item.split('$')
                    dict1[item_list[0]] = int(item_list[1])
        return dict1

    def test_hs_contact_rename(self):
        """重命名目标"""
        # 获取所有探测目标
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        # 将目标重命名为'敌机1'
        contact.hs_contact_rename('敌机1')
        self.env.step()
        self.assertEqual(contact.strName, '敌机1')

    def test_hs_contact_drop_target(self):
        """放弃目标"""

        # 设置对空限制开火
        side_doctrine = self.red_side.get_doctrine()
        side_doctrine.set_weapon_control_status('weapon_control_status_air', 2)

        # 向敌机1发射一枚 MIM-104B型“爱国者-1”防空导弹
        weapon_guid = 'hsfw-dataweapon-00000000001152'
        self.ground_to_air_missile_squadron.allocate_weapon_to_target(self.enemy_airplane_guid, weapon_guid, 1)

        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        # 放弃目标
        contact.hs_contact_drop_target()

        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
                break
        self.assertEqual(False, flag)

    def test_hs_contact_filter_target(self):
        """过滤目标"""
        contact = self.red_side.get_contacts()[self.enemy_airplane_guid]
        # 过滤目标
        contact.hs_contact_drop_target()
        self.env.step()

