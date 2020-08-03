from .models import PhaseLightRelation, LightRoadRelation, CustSignalInterMap, PhaseFroadFTRidMap
from .tools import find_froad_id, find_troad_id, find_turn, get_dir_name, get_turn_name

import itertools


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


# 计算所有相位的排列组合
def get_phase_plan_list(cust_signal_id, start_index):

    phsase_light_list = PhaseLightRelation.objects.filter(cust_signal_id=cust_signal_id)

    phase_content = ''

    for phase_light in phsase_light_list:
        if phase_light.phase_name in phase_content:
            continue
        else:
            phase_content += phase_light.phase_name

    phase_plan_list = []
    phase_plan_id = start_index
    for i in range(2, len(phase_content) + 1):
        phase_comb = itertools.combinations(phase_content, i)

        for j in phase_comb:
            phase_plan_dict = {'phase_plan_id': phase_plan_id, 'phase_content': j}
            phase_plan_list.append(phase_plan_dict)

            phase_plan_id += 1

    return phase_plan_list


# 计算phase_dir
def get_phase_dir(inter_id):
    # 查询路口名称
    inter_info = CustSignalInterMap.objects.get(inter_id=inter_id)
    inter_name = inter_info.inter_name

    phase_road_ft_rid_list = PhaseFroadFTRidMap.objects.filter(inter_id=inter_id, f_rid__isnull=False)

    # 相位通行方向列表
    phase_dir_list = []

    # 根据通行内容取道路信息
    for phase_road_ft_rid in phase_road_ft_rid_list:

        # 计算进口道方向
        dir_name = get_dir_name(phase_road_ft_rid.f_rid.ft_dir_4_no)

        # 计算转向描述
        turn_name = get_turn_name(phase_road_ft_rid.turn_dir_no)

        phase_dir_dict = {'inter_id': inter_id,
                          'inter_name': inter_name,
                          'phase_name': phase_road_ft_rid.phase_name,
                          'dir_name': dir_name + '_' + turn_name,
                          'f_rid': phase_road_ft_rid.f_rid_id,
                          't_rid': phase_road_ft_rid.t_rid_id,
                          'f_dir_4_no': phase_road_ft_rid.f_rid.ft_dir_4_no,
                          'f_dir_8_no': phase_road_ft_rid.f_rid.rid_dir_8_no,
                          'turn_dir_no': int(phase_road_ft_rid.turn_dir_no),
                          }

        phase_dir_list.append(phase_dir_dict)

    return phase_dir_list


# 生成相位方案的phase_dir
def get_phase_dir_multi_plan(inter_id, start_index):
    # 查找scats_id
    try:
        cust_signal_inter = CustSignalInterMap.objects.get(inter_id=inter_id)
    except Exception as e:
        print('%r: %r' % (e, inter_id))

        return None

    cust_signal_id = cust_signal_inter.cust_inter_id

    # 获取路口相位id列表
    phase_plan_list = get_phase_plan_list(cust_signal_id, start_index)
    # 获取路口相位通行方向数据列表
    phase_dir_list = get_phase_dir(inter_id)

    phase_dir_multi_plan_list = []

    for phase_plan in phase_plan_list:
        phase_plan_id = phase_plan.get('phase_plan_id')

        # 相位内容
        for phase_name in phase_plan.get('phase_content'):

            # 相位通行方向
            for phase_dir in phase_dir_list:
                if phase_name == phase_dir.get('phase_name'):

                    phase_plan_dir = {'phase_plan_id': phase_plan_id,
                                      'inter_id': phase_dir.get('inter_id'),
                                      'inter_name': phase_dir.get('inter_name'),
                                      'phase_name': phase_dir.get('phase_name'),
                                      'dir_name': phase_dir.get('dir_name'),
                                      'f_rid': phase_dir.get('f_rid'),
                                      't_rid': phase_dir.get('t_rid'),
                                      'f_dir_4_no': phase_dir.get('f_dir_4_no'),
                                      'f_dir_8_no': phase_dir.get('f_dir_8_no'),
                                      'turn_dir_no': phase_dir.get('turn_dir_no'),
                                      }

                    phase_dir_multi_plan_list.append(phase_plan_dir)
                else:
                    continue

    return phase_dir_multi_plan_list





















