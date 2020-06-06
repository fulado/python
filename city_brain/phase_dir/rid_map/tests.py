import sys
import os
import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phase_dir.settings')
django.setup()

from rid_map.models import PhaseLightRelation, LightRoadRelation, CustSignalInterMap, PhaseFroadFTRidMap
from rid_map.tools_phase import get_phase_plan_list, save_phase_cust_road, get_phase_dir, get_phase_plan_dir
from rid_map.odps_io import write_inter_phase_data_into_odps

import pprint

# 写入电科phase_dir数据到mysql数据库
# 导入新的区数据后都要生成一遍, 后续才可以做数据映射
def save_cust_phase_dir(area_code):
    inter_list = CustSignalInterMap.objects.filter(area_code=area_code).values('inter_id').distinct()

    for inter_id in inter_list:
        res = save_phase_cust_road(inter_id.get('inter_id'))
        print(inter_id.get('inter_id') + str(res))


# 写入根据区号写入inter_phase数据到odps
def write_inter_phase_data():
    area_code = '310104'
    start_index = 10
    write_inter_phase_data_into_odps(area_code, start_index)


if __name__ == '__main__':
    write_inter_phase_data()
    inter_id = '151LN09GHS0'
    phase_plan_dir_list = get_phase_plan_dir(inter_id)

    pprint.pprint(phase_plan_dir_list)


