from .models import PhaseLightRelation, LightRoadRelation, CustSignalInterMap, PhaseFroadFTRidMap
from .tools import find_froad_id, find_troad_id, find_turn


# 根据电科路口id获取电科的相位与灯组关系数据
def get_cust_phase_light(cust_signal_id):
    # 取路口相位与灯组的关系
    phase_light_list = PhaseLightRelation.objects.filter(cust_signal_id=cust_signal_id)

    # 相位通行灯组列表
    phase_light_dict_list = []

    # 生成相位与灯组id列表
    for phase_light_info in phase_light_list:

        phase_name = phase_light_info.phase_name
        light_list = phase_light_info.lightset_id_list.split(',')

        for light_id in light_list:
            data_dict = {'phase_name': phase_name, 'light_id': light_id}

            phase_light_dict_list.append(data_dict)

    return phase_light_dict_list


#  根据电科路口id获取电科的灯组通行内容数据
def get_cust_light_content(cust_signal_id):
    # 相位灯组信息列表
    light_content_dict_list = []

    light_content_list = LightRoadRelation.objects.filter(cust_signal_id=cust_signal_id)

    for light_content in light_content_list:
        data_dict = {'light_id': light_content.lightset_id,
                     'light_content': light_content.lightset_content,
                     }

        light_content_dict_list.append(data_dict)

    return light_content_dict_list


# 生成路口相位与电科进口道关系
def gen_phase_cust_road(cust_signal_id):
    phase_light_dict_list = get_cust_phase_light(cust_signal_id)
    light_content_dict_list = get_cust_light_content(cust_signal_id)

    # 相位通行方向列表
    phase_cust_road_list = []

    for phase_light_dict in phase_light_dict_list:
        for light_content_dict in light_content_dict_list:
            # print(phase_light_dict)
            # print(light_content_dict)
            if light_content_dict.get('light_id') == phase_light_dict.get('light_id'):
                light_content = light_content_dict.get('light_content')
                phase_cust_road = {'phase_name': phase_light_dict.get('phase_name'),
                                   'light_id': light_content_dict.get('light_id'),
                                   'f_road': find_froad_id(light_content),
                                   't_road': find_troad_id(light_content),
                                   'cust_turn': find_turn(light_content),
                                   }

                phase_cust_road_list.append(phase_cust_road)

    return phase_cust_road_list


# 写入路口相位与电科进口道数据到数据表
def save_phase_cust_road(inter_id):
    try:
        cust_signal_inter_list = CustSignalInterMap.objects.filter(inter_id=inter_id)
    except Exception as e:
        print(e)
        return False

    cust_signal_inter = cust_signal_inter_list[0]

    cust_singal_id = cust_signal_inter.cust_inter_id

    phase_cust_road_list = gen_phase_cust_road(cust_singal_id)

    for phase_cust_road in phase_cust_road_list:
        phase_road_rid_map = PhaseFroadFTRidMap()

        phase_road_rid_map.inter_id = inter_id
        phase_road_rid_map.phase_name = phase_cust_road.get('phase_name')
        phase_road_rid_map.f_road_id = cust_singal_id + phase_cust_road.get('f_road')
        phase_road_rid_map.cust_turn = phase_cust_road.get('cust_turn')

        if phase_cust_road.get('cust_turn') != '行人':
            phase_road_rid_map.t_road_id = cust_singal_id + phase_cust_road.get('t_road')
        else:
            pass

        try:
            phase_road_rid_map.save()
        except Exception as e:
            print(e)
            return False

    return True

















