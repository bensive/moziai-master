from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from mozi_ai_sdk.btmodel.bt.basic import *
from mozi_ai_sdk.btmodel.bt.detail import *
import geopy
from geopy import distance
from math import radians, cos, sin, asin, atan2, degrees

from absl import flags
from datetime import datetime


def print_arguments(flags_FLAGS):
    arg_name_list = dir(flags.FLAGS)
    black_set = {'alsologtostderr', 'log_dir', 'logtostderr', 'showprefixforinfo', 'stderrthreshold', 'v', 'verbosity',
                 '?', 'use_cprofile_for_profiling', 'help', 'helpfull', 'helpshort', 'helpxml', 'profile_file',
                 'run_with_profiling', 'only_check_args', 'pdb_post_mortem', 'run_with_pdb'}
    print("---------------------  Configuration Arguments --------------------")
    for arg_name in arg_name_list:
        if not arg_name.startswith('sc2_') and arg_name not in black_set:
            print("%s: %s" % (arg_name, flags_FLAGS[arg_name].value))
    print("-------------------------------------------------------------------")


def tprint(x):
    print("[%s] %s" % (str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), x))


def print_actions(env):
    print("----------------------------- Actions -----------------------------")
    for action_id, action_name in enumerate(env.action_names):
        print("Action ID: %d	Action Name: %s" % (action_id, action_name))
    print("-------------------------------------------------------------------")


def print_action_distribution(env, action_counts):
    print("----------------------- Action Distribution -----------------------")
    for action_id, action_name in enumerate(env.action_names):
        print("Action ID: %d	Count: %d	Name: %s" %
              (action_id, action_counts[action_id], action_name))
    print("-------------------------------------------------------------------")


def situationAwareness(side):
    # redside = scenario.get_side_by_name('蓝方')
    contacts = side.contacts
    mssnSitu = side.strikemssns
    patrolmssn = side.patrolmssns
    # targets = {k: v for k, v in contacts.items() if (('DDG' in v.strName) | ('CVN' in v.strName))}
    target = {k: v for k, v in contacts.items() if ('DDG' in v.strName)}
    if len(target) == 0:
        return False
    strkmssn = [v for v in mssnSitu.values() if v.strName == 'strike2'][0]

    # 获取任务执行单元
    missionUnits = strkmssn.m_AssignedUnits.split('@')
    create = False
    for unitGuid in missionUnits:
        check_unit_retreat_and_compute_retreat_pos(side, unitGuid)

        # TODO 切换任务
        # retreat, retreatPos = utils.check_unit_retreat_and_compute_retreat_pos(side, unitGuid)
        # if retreat == True:
        #     if len(strkPatrol) == 0 & create == False:
        #         pos = {}
        #         pos['latitude'] = list(target.values())[0].dLatitude
        #         pos['longitude'] = list(target.values())[0].dLongitude
        #         point_list = utils.create_patrol_zone(side, pos)
        #         postr = []
        #         for point in point_list:
        #             postr.append(point.strName)
        #         side.add_mission_patrol('strikePatrol', 1, postr)
        #         strikePatrolmssn = CPatrolMission('T+1_mode', scenario.mozi_server, scenario.situation)
        #         strikePatrolmssn.strName = 'strikePatrol'
        #         # 取消满足编队规模才能起飞的限制（任务条令）
        #         strikePatrolmssn.set_flight_size_check('红方', 'strikePatrol', 'false')
        #         utils.change_unit_mission(side, strkmssn, strikePatrolmssn, missionUnits)
        #         return True
        #     else:
        #         break


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
    if unit is None:
        return None, None
    else:
        unitPos['Latitude'] = unit.dLatitude
        unitPos['Longitude'] = unit.dLongitude

    for k, v in AirContacts.items():
        if v.m_IdentificationStatus >= 3:
            disKilo = get_two_point_distance(unitPos['Longitude'], unitPos['Latitude'], v.dLongitude,
                                             v.dLatitude)
            if disKilo <= v.fAirRangeMax * 1.852:  # 海里转公里需要乘以1.852
                # 计算撤退点 TODO
                doctrine = unit.get_doctrine()
                doctrine.ignore_plotted_course('yes')
                unit.set_unit_heading(unit.fCurrentHeading + 180)
                retreatPos = get_point_with_point_bearing_distance(unitPos['Longitude'], unitPos['Latitude'],
                                                                   unit.fCurrentHeading + 180, 10)
                unit.plot_course([retreatPos])

                return True, retreatPos
        else:
            continue
    return False, None


def get_point_with_point_bearing_distance(lat, lon, bearing, gap):
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
    disRatio = gap / radiusEarthKilometres
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
    # dic = {"latitude": my_lat, "longitude": my_lon}
    dic = (my_lat, my_lon)
    return dic


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
    dic = {"latitude": d.latitude, "longitude": d.longitude}
    return dic


# print(get_distance_point(33.0625105185452, 44.6287913650984, 40, 325))
# latitude='33.3681951159897', longitude='44.3768440602801'

def get_two_point_distance(lon1, lat1, lon2, lat2):
    pos1 = (lat1, lon1)
    pos2 = (lat2, lon2)
    dis = distance.vincenty(pos1, pos2)
    return dis.kilometers


def get_air_contacts(contacts):
    AirContacts = {}
    for k, v in contacts.items():
        if v.m_ContactType == 0:
            AirContacts[k] = v
    return AirContacts


def FindBoundingBoxForGivenContacts(contacts, defaults, padding):
    #  Variables
    coordinates = [btBas.MakeLatLong(defaults['AI-AO-1']['latitude'], defaults['AI-AO-1']['longitude']),
                   btBas.MakeLatLong(defaults['AI-AO-2']['latitude'], defaults['AI-AO-2']['longitude']),
                   btBas.MakeLatLong(defaults['AI-AO-3']['latitude'], defaults['AI-AO-3']['longitude']),
                   btBas.MakeLatLong(defaults['AI-AO-4']['latitude'], defaults['AI-AO-4']['longitude'])]
    contactBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 0)
    contactCoordinates = []

    for k, v in contacts.items():
        contact = {'latitude': v.dLatitude, 'longitude': v.dLongitude}
        contactCoordinates.append(btBas.MakeLatLong(contact['latitude'], contact['longitude']))

    # Get Hostile Contact Bounding Box
    if len(contactCoordinates) > 0:
        contactBoundingBox = FindBoundingBoxForGivenLocations(contactCoordinates, padding)

    # Return Bounding Box
    return contactBoundingBox


def FindBoundingBoxForGivenLocations(coordinates, padding):
    west = 0.0
    east = 0.0
    north = 0.0
    south = 0.0

    # Condiation Check
    if coordinates is None or len(coordinates) == 0:
        padding = 0

    # Assign Up to numberOfReconToAssign
    for lc in range(0, len(coordinates)):
        loc = coordinates[lc]
        if lc == 0:
            north = loc['latitude']
            south = loc['latitude']
            west = loc['longitude']
            east = loc['longitude']
        else:
            if loc['latitude'] > north:
                north = loc['latitude']
            elif loc['latitude'] < south:
                south = loc['latitude']

            if loc['longitude'] < west:
                west = loc['longitude']
            elif loc['longitude'] > east:
                east = loc['longitude']

    # Adding Padding
    north = north + padding
    south = south - padding
    west = west - padding
    east = east + padding

    # Return In Format
    return [MakeLatLong(north, west), MakeLatLong(north, east), MakeLatLong(south, east), MakeLatLong(south, west)]


def zone_contain_unit(zone, unit):
    if len(zone) < 4:
        raise IndexError

    temp = sorted(zone, key=lambda x: x['latitude'], reverse=True)
    temp_1 = sorted(temp[:2], key=lambda x: x['longitude'], reverse=False)
    temp_2 = sorted(temp[:2], key=lambda x: x['longitude'], reverse=True)
    zone = temp_1 + temp_2
    if (unit['latitude'] <= zone[0]['latitude']) and (unit['latitude'] >= zone[2]['latitude']):
        if (unit['longitude'] <= zone[1]['longitude']) and (unit['longitude'] >= zone[3]['longitude']):
            return True
        else:
            return False
    else:
        return False


def MakeLatLong(latitude, longitude):
    instance = {'latitude': InternationalDecimalConverter(latitude),
                'longitude': InternationalDecimalConverter(longitude)}
    return instance


# 三维地球上两点中间的坐标
def MidPointCoordinate(lat1, lon1, lat2, lon2):
    # initialize
    lat1 = InternationalDecimalConverter(lat1)
    lon1 = InternationalDecimalConverter(lon1)
    lat2 = InternationalDecimalConverter(lat2)
    lon2 = InternationalDecimalConverter(lon2)
    dLon = math.radians(lon2 - lon1)
    # convert to radians
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)

    Bx = math.cos(lat2) * math.cos(dLon)
    By = math.cos(lat2) * math.sin(dLon)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),
                      math.sqrt((math.cos(lat1) + Bx) * (math.cos(lat1) + Bx) + By * By))
    lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)

    return MakeLatLong(math.degrees(lat3), math.degrees(lon3))
