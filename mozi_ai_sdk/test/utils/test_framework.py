
import unittest
from mozi_ai_sdk.test.env.env import Environment
from mozi_ai_sdk.test.env import etc
import os


class TestFramework(unittest.TestCase):

    def setUp(self):
        print("--------------- CASE START ----------------------------")

        os.environ['MOZIPATH'] = etc.MOZI_PATH

        self.env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.SERVER_PLAT,
                               etc.SCENARIO_NAME_ACTIVE_UNIT_TEST, etc.SIMULATE_COMPRESSION,
                               etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.app_mode)
        # self.env = Environment(etc.SERVER_IP, etc.SERVER_PORT, duration_interval=etc.DURATION_INTERVAL, app_mode=3,
        #                   agent_key_event_file=None, request_id='红方')

        self.env.start()
        self.scenario = self.env.reset()
        self.red_side = self.scenario.get_side_by_name("红方")
        self.blue_side = self.scenario.get_side_by_name("蓝方")
        # 受油机
        self.refuel_aircraft = self.red_side.get_unit_by_guid('981d430b-23b9-4961-b179-d93d1e381294')
        # 加油机1
        self.refueling_tanker_aircraft_guid = 'c9e1d2c5-e80c-4105-aa37-6c69ded32786'
        self.refueling_tanker_aircraft = self.red_side.get_unit_by_guid(self.refueling_tanker_aircraft_guid)
        # 机场1
        self.airport_1_guid = 'b07b1274-09e3-4568-aa75-107a0a7fe2bf'
        self.airport_1 = self.red_side.get_unit_by_guid(self.airport_1_guid)
        # 机场2
        self.airport_2 = self.red_side.get_unit_by_guid('5f87395d-d4db-427a-8d9b-9c1d06e48273')
        # 码头1
        self.wharf_1_guid = '150eceac-e206-4394-a60f-263fa631e394'
        self.wharf_1 = self.red_side.get_unit_by_guid(self.wharf_1_guid)
        # 地空导弹中队
        self.ground_to_air_missile_squadron = self.red_side.get_unit_by_guid('fe0bd1ae-552a-49e1-b265-2f7ab8d0b60a')
        # 反潜机1
        self.antisubmarine_aircraft_guid = 'e85dc457-c49f-4ccd-84ee-36ec967fb0d4'
        self.antisubmarine_aircraft = self.red_side.get_unit_by_guid(self.antisubmarine_aircraft_guid)
        # 反潜机2
        self.antisubmarine_aircraft_2_guid = 'bc3c5422-471c-4ac7-a7d8-a8b50f032222'
        self.antisubmarine_aircraft_2 = self.red_side.get_unit_by_guid(self.antisubmarine_aircraft_2_guid)
        # 舰船-纯方位发射
        self.ship = self.red_side.get_unit_by_guid('482f6210-a205-4b06-9c39-1b8396ab798a')
        # 日本舰船1
        self.ship_japan_1_guid = '9ba83e41-5a07-4cf7-9533-911cffb41edc'
        self.ship_japan_1 = self.red_side.get_unit_by_guid(self.ship_japan_1_guid)
        # 舰船1 - 码头内
        self.docked_ship_1 = self.red_side.get_unit_by_guid('ec0cd2d6-236d-44e3-a223-859aedd6f62a')
        # 舰船2 - 码头内
        self.docked_ship_2 = self.red_side.get_unit_by_guid('33d7274a-0cbf-4c00-96e6-3c8b57bcfac9')
        # 舰船 - 投送
        self.ship_cargo = self.red_side.get_unit_by_guid('8e41ad3c-3048-4309-8bac-a36953c2c688')
        # F-35 #1 - 机场内
        self.docked_f35_1_guid = '775befba-9439-4818-9083-9f1907a4241d'
        self.docked_f35_1 = self.red_side.get_unit_by_guid(self.docked_f35_1_guid)
        # F-35 #2 - 机场内
        self.docked_f35_2_guid = '0589ad13-59ed-4b67-ad70-331ea61c7396'
        self.docked_f35_2 = self.red_side.get_unit_by_guid(self.docked_f35_2_guid)
        # 直升机-吊放声呐
        self.aircraft_dipping_sonar = self.red_side.get_unit_by_guid('973e3ee3-19b4-474e-ab22-e87a4510ce6d')
        # 飞机-投放声纳
        self.aircraft_drop_sonar_guid = '3e8e1341-2524-4024-981e-66a83a64c810'
        self.aircraft_drop_sonar = self.red_side.get_unit_by_guid(self.aircraft_drop_sonar_guid)
        groups = self.red_side.get_groups()
        # 编组- 飞行编队37
        self.air_group = groups['3f9f0353-15b0-4ce9-bb49-8c7d9252b072']
        # 反潜机3
        self.air_group_unit_guid_1 = '57d49860-5623-4146-aeb1-b91699c4fa90'
        self.antisubmarine_aircraft_3 = self.red_side.get_unit_by_guid(self.air_group_unit_guid_1)
        # 反潜机4
        self.air_group_unit_guid_2 = '676213d6-f063-4907-811f-308aba86ea6c'
        self.antisubmarine_aircraft_4 = self.red_side.get_unit_by_guid(self.air_group_unit_guid_2)
        # 编组- 日本舰队
        self.ship_group = groups['70e00c48-d2dc-44d1-b7fd-75cb59e60275']

        self.enemy_airplane_guid = '801ea534-a57c-4d3b-ba5d-0f77e909506c'
        self.enemy_airplane_guid_2 = '781cc773-30e3-440d-8750-1b5cddb90249'

        self.submarine_guid = '97d70ba0-89b7-4586-9d29-4399b823ebf0'
        self.submarine = self.red_side.get_unit_by_guid(self.submarine_guid)

        self.doctrine_owner = self.red_side
        # self.doctrine_owner = self.red_side.get_missions_by_name('水上巡逻')
        # self.doctrine_owner = self.air_group
        # self.doctrine_owner = self.ship
        self.doctrine = self.doctrine_owner.get_doctrine()

    def tearDown(self):
        print("--------------- CASE END ----------------------------")