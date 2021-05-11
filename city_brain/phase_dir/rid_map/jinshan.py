from .models import CustTimePlanJinshan, PhaseLightRelation, PhaseIdPhaseNoMapJinshan, CustSignalInterMap, \
    PhaseFroadFTRidMap
import json
import pprint


# 根据路口id处理配时方案数据
def get_time_plan(site_id):
    cust_time_plan_list = CustTimePlanJinshan.objects.filter(site_id=site_id)

    time_plan_list = []

    for cust_time_plan in cust_time_plan_list:
        site_id = cust_time_plan.site_id
        split_plan_no = cust_time_plan.split_plan_no
        cycle_time = cust_time_plan.cycle_time
        barrier_num = cust_time_plan.barrier_num
        barrier_list = json.loads(cust_time_plan.barrier_list)

        cal_time_plan(site_id, split_plan_no, cycle_time, barrier_num, barrier_list, time_plan_list)

    return time_plan_list


def get_phase_light(site_id):
    """根据路口id获取相位与灯组关系"""
    cust_phase_light_list = PhaseLightRelation.objects.filter(cust_signal_id=site_id)

    phase_light_list = []
    for cust_phase_light in cust_phase_light_list:
        phase_light = {'site_id': site_id,
                       'phase_id': cust_phase_light.phase_name,
                       'light_list': cust_phase_light.lightset_id_list
                       }

        phase_light_list.append(phase_light)

        # print(phase_light)

    return phase_light_list


# 计算一套配时方案
def cal_time_plan(site_id, split_plan_no, cycle_time, barrier_num, barrier_list, time_plan_list):

    for barrier in barrier_list:
        for ring in barrier.get('ringList'):
            phase_time_sum = 0

            for phase in ring.get('phaseList'):
                phase_time_sum += phase.get('phaseTime')

                cust_time_plan_dict = {'site_id': site_id,
                                       'split_plan_no': split_plan_no,
                                       'cycle_time': cycle_time,
                                       'barrier_num': barrier_num,
                                       'barrier_no': barrier.get('barrierNo'),
                                       'ring_no': ring.get('ringNo'),
                                       'phase_id': phase.get('phaseId'),
                                       'phase_time': phase.get('phaseTime'),
                                       'phase_time_sum': phase_time_sum
                                       }

                if site_id[1] == '1':
                    cust_time_plan_dict['phase_name'] = phase.get('phaseNo')

                time_plan_list.append(cust_time_plan_dict)


def gen_phase_id_no_map(site_id):
    """计算路口配时方案并关联到灯组"""
    time_plan_list = get_time_plan(site_id)
    phase_light_list = get_phase_light(site_id)

    for time_plan in time_plan_list:
        phase_id_no_map = PhaseIdPhaseNoMapJinshan()
        phase_id_no_map.site_id = site_id
        phase_id_no_map.split_plan_no = time_plan.get('split_plan_no', None)
        phase_id_no_map.phase_id = time_plan.get('phase_id', None)
        phase_id_no_map.phase_no = time_plan.get('phase_name', None)

        for phase_light in phase_light_list:
            if time_plan.get('phase_id') == phase_light.get('phase_id'):
                phase_id_no_map.light_list = phase_light.get('light_list')
                break
        phase_id_no_map.save()
    print(site_id)


def save_phase_id_no_map():
    """保存相位id与no对应关系到数据库"""
    phase_id_no_list = CustSignalInterMap.objects.filter(area_code='310116', cust_inter_id__startswith='81').\
        order_by('cust_inter_id')

    for phase_id_no in phase_id_no_list:
        gen_phase_id_no_map(phase_id_no.cust_inter_id)


def test_jinshan():
    inter_id = '1510409C6F0'

    phase_road_ft_rid_list = PhaseFroadFTRidMap.objects.filter(inter_id=inter_id, f_rid__isnull=False).\
        exclude(f_rid=r'\N')

    print(len(phase_road_ft_rid_list))

    for phase_item in phase_road_ft_rid_list:
        print(phase_item.inter_id, phase_item.phase_name, phase_item.f_rid)


