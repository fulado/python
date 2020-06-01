from .models import PhaseLightRelation, LightRoadRelation


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


    # # 相位通行方向列表
    # phase_dir_list = []
    #
    # # 根据通行内容取道路信息
    # for phase_light_info in phase_light_info_dict_list:
    #     light_content = phase_light_info.get('light_content')
    #
    #     f_id = find_froad_id(light_content)  # 进口道
    #     t_id = find_troad_id(light_content)  # 出口道
    #     turn = find_turn(light_content)  # 转向描述
    #
    #     f_road_info = CustFroad.objects.get(cust_signal_id=cust_signal_id, cust_froad_id=f_id)
    #     t_road_info = CustFroad.objects.get(cust_signal_id=cust_signal_id, cust_froad_id=t_id)
    #
    #     phase_dir_dict = {'phase_name': phase_light_info.get('phase_name'),
    #                       'light_id': phase_light_info.get('light_id'),
    #                       'f_road': f_road_info.cust_froad_name + ' - ' + str(f_road_info.cust_froad_angle) + ' - ' +
    #                       f_road_info.cust_froad_id,
    #                       't_road': t_road_info.cust_froad_name + ' - ' + str(t_road_info.cust_froad_angle) + ' - ' +
    #                       t_road_info.cust_froad_id,
    #                       'turn': turn,
    #                       }
    #
    #     phase_dir_list.append(phase_dir_dict)
    #
    # return phase_dir_list