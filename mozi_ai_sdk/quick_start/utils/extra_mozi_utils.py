# 时间 : 2021/09/28 19:13
# 作者 : 张志高
# 文件 : extra_mozi_utils
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

from mozi_utils import geo

os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_02,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

# 获取本方机场
facilities = red_side.get_facilities()
airport = common.get_obj_by_name(facilities, '机场1')

# 根据距离和方位生成参考点
for i in range(6):
    point_lat_lon = geo.get_point_with_point_bearing_distance(airport.dLatitude, airport.dLongitude, 60 * i, 100)
    red_side.add_reference_point(f'新参考点-{i}', point_lat_lon['latitude'], point_lat_lon['longitude'])

# 获取两点间的距离
env.step()
rp_1 = red_side.get_reference_point_by_name('新参考点-1')
print(geo.get_two_point_distance(airport.dLongitude, airport.dLatitude, rp_1.dLongitude, rp_1.dLatitude))
pass

# 获取两点间的夹角
env.step()
print(geo.get_degree(airport.dLatitude, airport.dLongitude, rp_1.dLatitude, rp_1.dLongitude))
print(geo.get_degree(rp_1.dLatitude, rp_1.dLongitude, airport.dLatitude, airport.dLongitude))
pass

# 生成矩形阵列
rp_5 = red_side.get_reference_point_by_name('新参考点-5')
rp_2 = red_side.get_reference_point_by_name('新参考点-2')
geo.plot_square(4, red_side, (rp_5.dLatitude, rp_5.dLongitude), (rp_2.dLatitude, rp_2.dLongitude))
pass

# 给出画的网格，然后给一个坐标，返回这个坐标所在表格的中心点坐标
rp_5 = red_side.get_reference_point_by_name('新参考点-5')
rp_2 = red_side.get_reference_point_by_name('新参考点-2')
red_side.add_reference_point(f'给定坐标', rp_2.dLatitude + 1, rp_2.dLongitude - 1)
lat, lon = geo.get_cell_middle(4, (rp_5.dLatitude, rp_5.dLongitude), (rp_2.dLatitude, rp_2.dLongitude),
                               (rp_2.dLatitude + 1, rp_2.dLongitude - 1))
red_side.add_reference_point(f'中心点坐标', lat, lon)

pass
