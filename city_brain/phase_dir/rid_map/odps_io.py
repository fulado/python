from .models import CustSignalInterMap
from .tools_phase import get_phase_plan_list
from .tools_odps import delete_partition, write_data_into_odps

import pprint


# 写入inter_phase数据到odps
def write_inter_phase_data_into_odps(area_code, start_index):
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

    pprint.pprint(phase_plan_content_list)

    table_name = 'dwd_tfc_rltn_inter_phase_city_brain'
    partition = 'adcode=310000'

    # 删除分区
    delete_partition(table_name, partition)

    # 写入新数据
    # write_data_into_odps(table_name, partition, phase_plan_content_list)

    print('inter_phase数据写入完毕')
