# 时间 ： 2020/7/29 10:23
# 作者 ： Dixit
# 文件 ： utils.py
# 项目 ： moziAI
# 版权 ： 北京华戍防务技术有限公司

from mozi_ai_sdk.btmodel.bt.basic import *
from mozi_ai_sdk.btmodel.bt.detail import *
import geopy
from geopy import distance
from math import radians, cos, sin, asin, sqrt, degrees, atan2, degrees
# from mozi_utils.geo import get_two_point_distance


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


def get_distance_point(lat, lon, dis, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param dis: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = distance.VincentyDistance(kilometers=dis)
    d = d.destination(point=start, bearing=direction)
    print(d.latitude, d.longitude)
    # dic = {"latitude": d.latitude, "longitude": d.longitude}
    return d.latitude, d.longitude
# print(get_distance_point(33.0625105185452, 44.6287913650984, 40, 325))
# latitude='33.3681951159897', longitude='44.3768440602801'


def get_two_point_distance(lon1, lat1, lon2, lat2):
    pos1 = (lat1, lon1)
    pos2 = (lat2, lon2)
    dis = distance.vincenty(pos1, pos2)
    return dis.kilometers


def g_get_two_point_distance(lon1, lat1, lon2, lat2):
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


def get_air_contacts(contacts):
    AirContacts = {}
    for k, v in contacts.items():
        if v.m_ContactType == 0:
            AirContacts[k] = v
    return AirContacts


def check_unit_retreat_and_compute_retreat_pos(side, unit_guid):
    contacts = side.contacts
    # miss_dic = side.missions
    airs_dic = side.aircrafts
    AirContacts = get_air_contacts(contacts)
    unit = None
    for k, v in airs_dic.items():
        if k == unit_guid:
            unit = v
            break
    unitPos = {}
    if unit == None:
        return None, None
    else:
        unitPos['Latitude'] = unit.dLatitude
        unitPos['Longitude'] = unit.dLongitude

    for k, v in AirContacts.items():
        if v.m_IdentificationStatus >= 3:
            disKilo = g_get_two_point_distance(unitPos['Longitude'], unitPos['Latitude'], v.dLongitude,
                                             v.dLatitude)
            if disKilo <= v.fAirRangeMax * 1.852:  # 海里转公里需要乘以1.852
                # 计算撤退点 TODO
                # doctrine = unit.get_doctrine()
                # doctrine.ignore_plotted_course('yes')
                # # latitude = '25.5307909534701', longitude = '153.239828460436'
                # Heading = get_degree(25.5307909534701, 153.239828460436, unitPos['Latitude'], unitPos['Longitude'])
                # # unit.set_unit_heading(unit.fCurrentHeading + 180)
                # retreatPos = get_distance_point(unitPos['Latitude'], unitPos['Longitude'], 10, Heading)
                # unit.plot_course([retreatPos])
                mssnSitu = side.strikemssns
                strkmssn = [v for v in mssnSitu.values() if v.strGuid == unit.m_AssignedMission][0]
                print(unit.strName, '  ', strkmssn.strName)
                retreatPos = {'latitude': 25.5307909534701, 'longitude': 153.239828460436}

                return True, retreatPos
        else:
            continue
    return False, None


# 根据某点(比如撤退点)计算巡逻区 TODO
def create_patrol_zone(side, pos):

    lat = pos['latitude']
    lon = pos['longitude']
    # p1 = (lat - 0.10, lon - 0.13)
    # lat: 纬度， lon：经度
    rp1 = side.add_reference_point('strike_rp1', lat + 0.3, lon - 0.3)
    rp2 = side.add_reference_point('strike_rp2', lat + 0.3, lon + 0.3)
    rp3 = side.add_reference_point('strike_rp3', lat - 0.3, lon + 0.3)
    rp4 = side.add_reference_point('strike_rp4', lat - 0.3, lon - 0.3)
    point_list = [rp1, rp2, rp3, rp4]

    return point_list


def assign_planway_to_mission(side, mission_name, way_name, way_point_list, old_way_name=None):
    """
        给任务分配(重新分配)预设航线
    :param side: 方
    :param mission_name:任务
    :param way_name:预设航线名称
    :param way_point_list:
    :param old_way_name
    航线的航路点  [{}, {}, {}, ...]
    :return:
    任务类对象
    """

    side.add_plan_way(0, way_name)
    for point in way_point_list:
        side.add_plan_way_point(way_name, point['longitude'], point['latitude'])
    mission = side.get_missions_by_name(mission_name)
    if mission:
        mission.add_plan_way_to_mission(0, way_name)

    if old_way_name is not None:
        side.remove_plan_way(old_way_name)
    else:
        pass

# Hs_AddPlanWay('SideNameOrID',Type,'WayName')   添加预设航线
# Hs_AddPlanWayPoint('SideNameOrID','WayNameOrID',WayPointLongitude,WayPointLatitude)   为预设航线添加航路点
# Hs_UpDataPlanWayPoint('SideNameOrID','WayNameOrID','WayPointID',table)  为预设航线添加航路点
# Hs_UpDataPlanWayPoint('SideNameOrID','WayNameOrID','WayPointID',table)  修改预设航线的航路点
# Hs_RemovePlanWayPoint('SideNameOrID','WayNameOrID','WayPointID')    删除预设航线的航路点
# Hs_RemovePlanWay('SideNameOrID','WayNameOrID')   删除预设航线
# Hs_AddPlanWayToMission('MissionNameOrId',Type,'WayNameOrID')  为任务分配预设航线


def change_unit_mission(side, old_mission, new_mission, units):
    """
    改变一个或多个任务单元的任务
    :param side: 方
    :param old_mission: 旧任务对象
    :param new_mission: 新任务对象
    :param units: 任务单元  [ ]
    :return:
    """
    for unit in units:
        old_mission.unassign_unit(unit)
        new_mission.assign_unit(unit)

# ScenEdit_UnAssignUnitFromMission ('AUNameOrID','MissionNameOrID')   任务中移除单元
# ScenEdit_AssignUnitToMission('AUNameOrID','MissionNameOrID')   为任务指定执行单元（方法一）
# Hs_AssignUnitListToMission('AULNameOrID','MissionNameOrID')   为任务指定执行单元（方法二）


def FindBoundingBoxForGivenContacts(side, padding = 10):
    contacts = side.contacts

    #  Variables
    defaults = [MakeLatLong(0., 0.), MakeLatLong(0., 1.), MakeLatLong(1., 1.),
                MakeLatLong(1., 0.)]
    coordinates = [btBas.MakeLatLong(defaults[0]['latitude'], defaults[0]['longitude']),
                   btBas.MakeLatLong(defaults[1]['latitude'], defaults[1]['longitude']),
                   btBas.MakeLatLong(defaults[2]['latitude'], defaults[2]['longitude']),
                   btBas.MakeLatLong(defaults[3]['latitude'], defaults[3]['longitude'])]
    contactBoundingBox = btBas.FindBoundingBoxForGivenLocations(coordinates, padding)
    contactCoordinates = []

    for k, v in contacts.items():
        contact = {}
        contact['latitude'] = v.dLatitude
        contact['longitude'] = v.dLongitude
        contactCoordinates.append(btBas.MakeLatLong(contact['latitude'], contact['longitude']))

    # Get Hostile Contact Bounding Box
    if len(contactCoordinates) > 0:
        contactBoundingBox = FindBoundingBoxForGivenLocations(contactCoordinates, padding)

    # Return Bounding Box
    return contactBoundingBox
