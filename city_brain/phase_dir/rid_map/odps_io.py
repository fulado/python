from .models import CustSignalInterMap
from .tools_phase import get_phase_plan_list, get_phase_dir_multi_plan, get_phase_dir
from .tools_odps import delete_partition, write_data_into_odps

import time


# 写入inter_phase数据到odps
def write_inter_phase_into_odps(area_code, start_index):
    # 查询某一区全部路口inter_id
    cust_signal_inter_map_list = CustSignalInterMap.objects.filter(area_code=area_code)

    phase_plan_content_list = []

    for cust_signal_inter_map in cust_signal_inter_map_list:

        inter_id = cust_signal_inter_map.inter_id
        cust_inter_id = cust_signal_inter_map.cust_inter_id
        phase_plan_list = get_phase_plan_list(cust_inter_id, start_index)

        for phase_plan in phase_plan_list:
            phase_plan_content = [inter_id,
                                  cust_inter_id,
                                  ','.join(phase_plan.get('phase_content')),
                                  len(phase_plan.get('phase_content')),
                                  str(phase_plan.get('phase_plan_id')),
                                  '',
                                  '310000'
                                  ]

            phase_plan_content_list.append(phase_plan_content)

    table_name = 'dwd_tfc_rltn_inter_phase_city_brain'
    partition = 'area_code=' + area_code

    # 删除分区
    delete_partition(table_name, partition)

    # 写入新数据
    # print(phase_plan_content_list)
    write_data_into_odps(table_name, partition, phase_plan_content_list)

    print('inter_phase数据写入完毕')


# 写入phase_dir数据到odps
def write_phase_dir_into_odps(area_code, start_index):
    """
    :param area_code: 区域代码
    :param start_index: phase_plan_id开始值, 建议每次重新写入时都在上一次start_index的值上增加至少50
    :return:
    """
    phase_dir_list = []

    if area_code == '310116_junma':
        inter_id_list = CustSignalInterMap.objects.filter(area_code='310116', cust_inter_id__startswith='80').\
            values('inter_id').distinct()
    elif area_code == '310116_qingyi':
        inter_id_list = CustSignalInterMap.objects.filter(area_code='310116', cust_inter_id__startswith='81').\
            values('inter_id').distinct()
    else:
        inter_id_list = CustSignalInterMap.objects.filter(area_code=area_code).values('inter_id').distinct()

    for inter_id in inter_id_list:
        if area_code == '310116_junma' or area_code == '310116_qingyi':
            single_inter_phase_dir_list = get_phase_dir(inter_id.get('inter_id', ''))
        else:
            single_inter_phase_dir_list = get_phase_dir_multi_plan(inter_id.get('inter_id', ''), start_index)

        for single_inter_phase_dir in single_inter_phase_dir_list:
            phase_plan_content = [single_inter_phase_dir.get('inter_id', None),
                                  single_inter_phase_dir.get('inter_name', None),
                                  single_inter_phase_dir.get('phase_plan_id', '1'),
                                  single_inter_phase_dir.get('phase_name', None),
                                  single_inter_phase_dir.get('dir_name', None),
                                  single_inter_phase_dir.get('f_rid', None),
                                  single_inter_phase_dir.get('t_rid', None),
                                  single_inter_phase_dir.get('f_dir_4_no', None),
                                  single_inter_phase_dir.get('f_dir_8_no', None),
                                  single_inter_phase_dir.get('turn_dir_no', None),
                                  '20171231',
                                  time.strftime('%Y%m%d', time.localtime()),
                                  'scats',
                                  time.strftime('%Y%m%d', time.localtime()),
                                  '310000'
                                  ]

            phase_dir_list.append(phase_plan_content)

    table_name = 'dwd_tfc_ctl_signal_phasedir_city_brain'
    partition = 'area_code=' + area_code

    # 删除分区
    delete_partition(table_name, partition)

    # 写入新数据
    # print(phase_dir_list)
    write_data_into_odps(table_name, partition, phase_dir_list)

    print('phase_dir数据写入完毕')














