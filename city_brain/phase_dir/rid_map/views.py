from django.shortcuts import render
from django.http import JsonResponse
from .models import CustFroad, InterRid, InterOutRid, RoadRidMap, RoadOutRidMap, CustSignalInterMap, \
    PhaseLightRelation, LightRoadRelation
from .tools import find_froad_id, find_troad_id, find_turn, get_dir_name, get_turn_dir_no
from .tools_odps import write_data_into_odps, delete_partition
import xlwt
import time
import pprint


# Create your views here.


def select(request):
    return render(request, 'select.html')


def main(request):
    ft = int(request.GET.get('ft', 1))  # 进出口道标志位, 1-进口道, 2-出口道

    request.session['ft'] = ft

    inter_list_baoshan = CustSignalInterMap.objects.filter(area_code='310113').order_by('cust_inter_id')
    inter_list_hongkou = CustSignalInterMap.objects.filter(area_code='310109').order_by('cust_inter_id')
    inter_list_chongming = CustSignalInterMap.objects.filter(area_code='310151').order_by('cust_inter_id')
    inter_list_xuhui = CustSignalInterMap.objects.filter(area_code='310104').order_by('cust_inter_id')
    inter_list_yangpu = CustSignalInterMap.objects.filter(area_code='310110').order_by('cust_inter_id')

    context = {'inter_list_baoshan': inter_list_baoshan,
               'inter_list_hongkou': inter_list_hongkou,
               'inter_list_chongming': inter_list_chongming,
               'inter_list_xuhui': inter_list_xuhui,
               'inter_list_yangpu': inter_list_yangpu,
               }

    return render(request, 'main.html', context)


def rid_map_show(request):
    inter_id = request.GET.get('inter_id', '')
    rid_type = int(request.GET.get('rid_type', 1))

    ft = request.session.get('ft', 1)

    inter_map_info = CustSignalInterMap.objects.get(inter_id=inter_id)

    cust_signal_id = inter_map_info.cust_inter_id
    cust_froad_list = CustFroad.objects.filter(cust_signal_id=cust_signal_id)

    if ft == 2:
        rid_list = InterOutRid.objects.filter(inter_id=inter_id)
        map_list = RoadOutRidMap.objects.filter(inter_id=inter_id)
    else:
        rid_list = InterRid.objects.filter(inter_id=inter_id)
        map_list = RoadRidMap.objects.filter(inter_id=inter_id)

    if rid_type:
        rid_list = rid_list.filter(rid_type_no=rid_type)

    # 获取电科相位方向数据
    cust_phase_dir_list = get_cust_phase(cust_signal_id)

    context = {'cust_froad_list': cust_froad_list,
               'rid_list': rid_list,
               'map_list': map_list,
               'inter_id': inter_id,
               'inter_name': inter_map_info.inter_name,
               'cust_signal_id': cust_signal_id,
               'rid_type': rid_type,
               'cust_phase_dir_list': cust_phase_dir_list,
               }

    response = render(request, 'froad_rid.html', context)
    response.__setitem__('X-Frame-Options', 'ALLOW-FROM')

    return response


# 获取电科路段信息
def get_road_info(request):
    road_id = request.POST.get('road_id', '')

    try:
        road_info = CustFroad.objects.get(id=road_id)

        res = {'angle': road_info.cust_froad_angle,
               'name': road_info.cust_froad_name,
               }
    except:
        res = {'angle': '',
               'name': '',
               }

    return JsonResponse(res)


# 获取rid信息
def get_rid_info(request):
    rid_id = request.POST.get('rid_id', '')
    ft = request.session.get('ft', 1)

    try:
        if ft == 2:
            rid_info = InterOutRid.objects.get(rid=rid_id)
        else:
            rid_info = InterRid.objects.get(rid=rid_id)

        res = {'angle': rid_info.ft_angle,
               'name': rid_info.rid_name,
               }
    except:
        res = {'angle': '',
               'name': '',
               }

    return JsonResponse(res)


# 保存对应关系数据
def save_map(request):
    road_id = request.POST.get('road_id', '')
    rid_id = request.POST.get('rid_id', '')
    inter_id = request.POST.get('inter_id', '')
    ft = request.session.get('ft', 1)
    print(ft)
    if road_id != '' and rid_id != '':
        if ft == 2:
            road_rid_map = RoadOutRidMap()
        else:
            road_rid_map = RoadRidMap()

        road_rid_map.road_id = road_id
        road_rid_map.rid_id = rid_id
        road_rid_map.inter_id = inter_id

        road_info = CustFroad.objects.get(id=road_id)
        road_rid_map.cust_froad_id = road_info.cust_froad_id
        road_rid_map.cust_signal_id = road_info.cust_signal_id

        road_rid_map.save()

        map_id = road_rid_map.id
        res = {'map_id': map_id}
    else:
        res = {}

    return JsonResponse(res)


# 删除对应关系
def delete_map(request):
    map_id = request.POST.get('map_id', '')
    ft = request.session.get('ft', 1)

    try:
        if ft == 2:
            road_rid_map = RoadOutRidMap.objects.get(id=map_id)
        else:
            road_rid_map = RoadRidMap.objects.get(id=map_id)

        road_rid_map.delete()
    except:
        pass

    res = {}

    return JsonResponse(res)


# 生成phase_dir
def gen_phase_dir(request):
    # 创建excel
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)

    # 设置表头
    title = ['inter_id',
             'inter_name',
             'phase_plan_id',
             'phase_name',
             'dir_name',
             'f_rid',
             't_rid',
             'f_dir_4_no',
             'f_dir_8_no',
             'turn_dir_no',
             'data_version',
             'modified_date',
             'source',
             'start_date',
             'adcode',
             ]

    # 生成表头
    len_col = len(title)
    for i in range(0, len_col):
        ws.write(0, i, title[i])

    # 查询某一区全部路口inter_id
    cust_signal_inter_map_list = CustSignalInterMap.objects.filter(area_code='310109')

    i = 1
    for cust_signal_inter_map in cust_signal_inter_map_list:
        phase_dir_list = get_phase_dir(cust_signal_inter_map.inter_id)

        for phase_dir in phase_dir_list:
            ws.write(i, 0, phase_dir.get('inter_id'))
            ws.write(i, 1, phase_dir.get('inter_name'))
            ws.write(i, 2, '1')
            ws.write(i, 3, phase_dir.get('phase_name'))
            ws.write(i, 4, phase_dir.get('dir_name'))
            ws.write(i, 5, phase_dir.get('f_road'))
            ws.write(i, 6, phase_dir.get('t_road'))
            ws.write(i, 7, phase_dir.get('f_dir_4_no'))
            ws.write(i, 8, phase_dir.get('rid_dir_8_no'))
            ws.write(i, 9, phase_dir.get('turn_dir_no'))
            ws.write(i, 10, '20171231')
            ws.write(i, 11, time.strftime('%Y%m%d', time.localtime()))
            ws.write(i, 12, '人工录入')
            ws.write(i, 13, time.strftime('%Y%m%d', time.localtime()))
            ws.write(i, 14, '310000')

            i += 1

    wb.save('d:/phase_dir.xls')


# 获取电科的相位通行数据
def get_cust_phase(cust_signal_id):
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

    # 相位灯组信息列表
    phase_light_info_dict_list = []

    # 根据灯组id取通行内容
    for phase_light_dict in phase_light_dict_list:

        light_id = phase_light_dict.get('light_id')

        light_set_list = LightRoadRelation.objects.filter(cust_signal_id=cust_signal_id, lightset_id=light_id). \
            exclude(lightset_content__contains='行人')

        # 忽略行人相位
        if len(light_set_list) == 0:
            continue

        for light_set in light_set_list:
            data_dict = {'phase_name': phase_light_dict.get('phase_name'),
                         'light_id': phase_light_dict.get('light_id'),
                         'light_content': light_set.lightset_content.strip().replace(' ', ''),
                         }

            phase_light_info_dict_list.append(data_dict)

    # 相位通行方向列表
    phase_dir_list = []

    # 根据通行内容取道路信息
    for phase_light_info in phase_light_info_dict_list:
        light_content = phase_light_info.get('light_content')

        f_id = find_froad_id(light_content)  # 进口道
        t_id = find_troad_id(light_content)  # 出口道
        turn = find_turn(light_content)  # 转向描述

        f_road_info = CustFroad.objects.get(cust_signal_id=cust_signal_id, cust_froad_id=f_id)
        t_road_info = CustFroad.objects.get(cust_signal_id=cust_signal_id, cust_froad_id=t_id)

        phase_dir_dict = {'phase_name': phase_light_info.get('phase_name'),
                          'light_id': phase_light_info.get('light_id'),
                          'f_road': f_road_info.cust_froad_name + ' - ' + str(f_road_info.cust_froad_angle) + ' - ' +
                          f_road_info.cust_froad_id,
                          't_road': t_road_info.cust_froad_name + ' - ' + str(t_road_info.cust_froad_angle) + ' - ' +
                          t_road_info.cust_froad_id,
                          'turn': turn,
                          }

        phase_dir_list.append(phase_dir_dict)

    return phase_dir_list


# 计算phase_dir
def get_phase_dir(inter_id):
    cust_signal_inter = CustSignalInterMap.objects.get(inter_id=inter_id)

    cust_signal_id = cust_signal_inter.cust_inter_id
    inter_name = cust_signal_inter.inter_name

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

    # 相位灯组信息列表
    phase_light_info_dict_list = []

    # 根据灯组id取通行内容
    for phase_light_dict in phase_light_dict_list:

        light_id = phase_light_dict.get('light_id')

        light_set_list = LightRoadRelation.objects.filter(cust_signal_id=cust_signal_id, lightset_id=light_id). \
            exclude(lightset_content__contains='行人')

        # 忽略行人相位
        if len(light_set_list) == 0:
            continue

        for light_set in light_set_list:
            data_dict = {'phase_name': phase_light_dict.get('phase_name'),
                         'light_id': phase_light_dict.get('light_id'),
                         'light_content': light_set.lightset_content.strip().replace(' ', ''),
                         }

            phase_light_info_dict_list.append(data_dict)

    # 相位同行方向列表
    phase_dir_list = []

    # 根据通行内容取道路信息
    for phase_light_info in phase_light_info_dict_list:
        light_content = phase_light_info.get('light_content')

        f_id = find_froad_id(light_content)  # 进口道
        t_id = find_troad_id(light_content)  # 出口道
        turn = find_turn(light_content)  # 转向描述

        try:
            road_rid_map = RoadRidMap.objects.get(inter_id=inter_id, cust_signal_id=cust_signal_id, cust_froad_id=f_id)
            road_out_rid_map = RoadOutRidMap.objects.get(inter_id=inter_id, cust_signal_id=cust_signal_id,
                                                         cust_froad_id=t_id)
        except:
            continue

        phase_dir_dict = {'inter_id': inter_id,
                          'inter_name': inter_name,
                          'phase_name': phase_light_info.get('phase_name'),
                          'dir_name': get_dir_name(road_rid_map.rid.ft_dir_4_no) + '_' + turn,
                          'f_road': road_rid_map.rid_id,
                          't_road': road_out_rid_map.rid_id,
                          'f_dir_4_no': road_rid_map.rid.ft_dir_4_no,
                          'f_dir_8_no': road_rid_map.rid.rid_dir_8_no,
                          'turn_dir_no': get_turn_dir_no(turn),
                          }

        phase_dir_list.append(phase_dir_dict)

    return phase_dir_list


# 导出phase_plan_id的phase_dir数据
def export_phase_plan_dir(request):

    # 创建excel
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)

    # 设置表头
    title = ['inter_id',
             'inter_name',
             'phase_plan_id',
             'phase_name',
             'dir_name',
             'f_rid',
             't_rid',
             'f_dir_4_no',
             'f_dir_8_no',
             'turn_dir_no',
             'data_version',
             'modified_date',
             'source',
             'start_date',
             'adcode',
             ]

    # 生成表头
    len_col = len(title)
    for i in range(0, len_col):
        ws.write(0, i, title[i])

    # 查询某一区全部路口inter_id
    cust_signal_inter_map_list = CustSignalInterMap.objects.filter(area_code='310109')

    i = 1
    for cust_signal_inter_map in cust_signal_inter_map_list:
        phase_plan_dir_list = gen_phase_dir_multi_plan(cust_signal_inter_map.inter_id)

        for phase_dir in phase_plan_dir_list:
            ws.write(i, 0, phase_dir.get('inter_id'))
            ws.write(i, 1, phase_dir.get('inter_name'))
            ws.write(i, 2, phase_dir.get('phase_plan_id'))
            ws.write(i, 3, phase_dir.get('phase_name'))
            ws.write(i, 4, phase_dir.get('dir_name'))
            ws.write(i, 5, phase_dir.get('f_road'))
            ws.write(i, 6, phase_dir.get('t_road'))
            ws.write(i, 7, phase_dir.get('f_dir_4_no'))
            ws.write(i, 8, phase_dir.get('f_dir_8_no'))
            ws.write(i, 9, phase_dir.get('turn_dir_no'))
            ws.write(i, 10, '20171231')
            ws.write(i, 11, time.strftime('%Y%m%d', time.localtime()))
            ws.write(i, 12, '人工录入')
            ws.write(i, 13, time.strftime('%Y%m%d', time.localtime()))
            ws.write(i, 14, '310000')

            i += 1

    wb.save('d:/phase_plan_dir.xls')


# 写入phase_dir数据到odps
def write_phase_dir_data_into_odps(request):

    table_name = 'dwd_tfc_ctl_signal_phasedir_baoshan'
    partition = 'adcode=310000'

    # 删除分区
    delete_partition(table_name, partition)

    # 查询某一区全部路口inter_id
    cust_signal_inter_map_list = CustSignalInterMap.objects.filter(area_code='310113')

    data_list = []
    for cust_signal_inter_map in cust_signal_inter_map_list:
        phase_plan_dir_list = gen_phase_dir_multi_plan(cust_signal_inter_map.inter_id)

        # data_list = []
        for phase_dir in phase_plan_dir_list:
            phase_dir_list = [phase_dir.get('inter_id'),
                              phase_dir.get('inter_name'),
                              phase_dir.get('phase_plan_id'),
                              phase_dir.get('phase_name'),
                              phase_dir.get('dir_name'),
                              phase_dir.get('f_road'),
                              phase_dir.get('t_road'),
                              int(phase_dir.get('f_dir_4_no')),
                              int(phase_dir.get('f_dir_8_no')),
                              int(phase_dir.get('turn_dir_no')),
                              '20171231',
                              time.strftime('%Y%m%d', time.localtime()),
                              '人工录入',
                              time.strftime('%Y%m%d', time.localtime()),
                              '310000',
                              ]

            data_list.append(phase_dir_list)

        # pprint.pprint(data_list)
        # break

    write_data_into_odps(table_name, partition, data_list)

    print('write odps ok')


# 写入inter_phase数据到odps
def write_inter_phase_data_into_odps(request):
    # 查询某一区全部路口inter_id
    cust_signal_inter_map_list = CustSignalInterMap.objects.filter(area_code__in=('310113', '310109'))

    phase_plan_content_list = []

    for cust_signal_inter_map in cust_signal_inter_map_list:

        cust_inter_id = cust_signal_inter_map.cust_inter_id
        phase_plan_list = get_phase_plan_list(cust_inter_id)

        for phase_plan in phase_plan_list:
            phase_plan_content = ['',
                                  cust_inter_id,
                                  ','.join(phase_plan.get('phase_content')),
                                  len(phase_plan.get('phase_content')),
                                  str(phase_plan.get('phase_plan_id')),
                                  '',
                                  '310000'
                                  ]

            phase_plan_content_list.append(phase_plan_content)

    # pprint.pprint(phase_plan_content_list)

    table_name = 'dwd_tfc_rltn_inter_phase_city_brain'
    partition = 'adcode=310000'

    # 删除分区
    delete_partition(table_name, partition)

    # 写入新数据
    write_data_into_odps(table_name, partition, phase_plan_content_list)

    print('inter_phase数据写入完毕')












