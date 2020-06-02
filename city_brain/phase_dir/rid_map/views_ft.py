from django.shortcuts import render
from django.http import JsonResponse
from .models import CustSignalInterMap, CustFroad, InterRid, InterOutRid, RoadFTRidMap, InterFTRid, PhaseFroadFTRidMap
from .views import get_cust_phase
from .phase_tools import save_phase_cust_road


def main(request):
    ft = int(request.GET.get('ft', 1))  # 进出口道标志位, 1-进口道, 2-出口道

    # request.session['ft'] = ft

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

    return render(request, 'main_ft.html', context)


def rid_map_show(request):
    inter_id = request.GET.get('inter_id', '')
    rid_type = int(request.GET.get('rid_type', 1))

    inter_map_info = CustSignalInterMap.objects.get(inter_id=inter_id)

    cust_signal_id = inter_map_info.cust_inter_id
    cust_froad_list = CustFroad.objects.filter(cust_signal_id=cust_signal_id)

    f_rid_list = InterRid.objects.filter(inter_id=inter_id)
    t_rid_list = InterOutRid.objects.filter(inter_id=inter_id)
    map_list = RoadFTRidMap.objects.filter(inter_id=inter_id)

    # ft_rid_list = InterFTRid.objects.filter(inter_id=inter_id)
    ft_f_rid_list = InterFTRid.objects.filter(inter_id=inter_id).values('f_road_name', 'f_angle', 'f_rid').distinct()

    if rid_type:
        f_rid_list = f_rid_list.filter(rid_type_no=rid_type)
        t_rid_list = t_rid_list.filter(rid_type_no=rid_type)

    # 获取电科相位方向数据
    phase_road_rid_list = PhaseFroadFTRidMap.objects.filter(inter_id=inter_id)

    context = {'cust_froad_list': cust_froad_list,
               'f_rid_list': f_rid_list,
               't_rid_list': t_rid_list,
               'map_list': map_list,
               'inter_id': inter_id,
               'inter_name': inter_map_info.inter_name,
               'cust_signal_id': cust_signal_id,
               'rid_type': rid_type,
               'phase_road_rid_list': phase_road_rid_list,
               # 'ft_rid_list': ft_rid_list,
               'ft_f_rid_list': ft_f_rid_list,
               }

    response = render(request, 'froad_rid_ft.html', context)
    response.__setitem__('X-Frame-Options', 'ALLOW-FROM')

    return response


# 获取ft_rid中的出口道rid
def get_t_rid_list(request):
    f_rid = request.POST.get('f_rid', '')

    ft_t_rid_list = InterFTRid.objects.filter(f_rid=f_rid).values('t_road_name', 't_angle', 't_rid').distinct()

    rid_list = []
    for t_rid in ft_t_rid_list:
        rid = {'t_rid_name_angle': t_rid.get('t_road_name') + '-' + str(t_rid.get('t_angle')),
               't_rid': t_rid.get('t_rid')}
        rid_list.append(rid)

    data = {'ft_t_rid_list': rid_list}

    return JsonResponse(data)


# 获取转向列表
def get_turn_list(request):
    f_rid = request.POST.get('f_rid', '')
    t_rid = request.POST.get('t_rid', '')

    ft_rid_list = InterFTRid.objects.filter(f_rid=f_rid, t_rid=t_rid)

    if len(ft_rid_list) == 1:
        ft_rid = ft_rid_list[0]

        if ft_rid.turn_dir_no == '1':
            turn_dir = '左转'
        elif ft_rid.turn_dir_no == '2':
            turn_dir = '直行'
        elif ft_rid.turn_dir_no == '3':
            turn_dir = '右转'
        elif ft_rid.turn_dir_no == '4':
            turn_dir = '掉头'
        else:
            turn_dir = '未知'

        data = {'turn_dir_no': ft_rid.turn_dir_no, 'turn_dir': turn_dir}
    else:
        data = {'id': 0, 'turn_dir': '错误'}

    return JsonResponse(data)


# 保存相位进口道rid对应关系数据
def add_map_ft(request):

    map_id = request.POST.get('map_id', '')
    f_rid = request.POST.get('f_rid', '')
    t_rid = request.POST.get('t_rid', '')
    turn_dir_no = request.POST.get('turn_dir_no', '')

    # print(map_id)
    # print(f_rid)
    # print(t_rid)
    # print(turn_dir_no)

    if turn_dir_no == '1':
        turn_dir = '左转'
    elif turn_dir_no == '2':
        turn_dir = '直行'
    elif turn_dir_no == '3':
        turn_dir = '右转'
    elif turn_dir_no == '4':
        turn_dir = '掉头'
    elif turn_dir_no == '0':
        turn_dir = '行人'
    else:
        turn_dir = '未知'

    # 根据map_id确定当前的PhaseFroadFTRidMap
    phase_road_ftrid = PhaseFroadFTRidMap.objects.get(id=map_id)

    phase_road_ftrid.f_rid_id = f_rid
    phase_road_ftrid.turn_dir_no = turn_dir_no

    if turn_dir_no == '0':  # 行人相位
        # 行人相位没有出口道, 只查询进口道
        f_rid_info = InterRid.objects.get(rid=f_rid)
        phase_road_ftrid.t_rid_id = None

        data = {'f_rid': f_rid_info.rid_name + ' - ' + str(f_rid_info.ft_angle),
                't_rid': '',
                'turn_dir': turn_dir,
                }
    else:
        phase_road_ftrid.t_rid_id = t_rid

        # 非行人相位, 根据f_rid, t_rid, turn_dir_no确定一条ft_rid
        ft_rid_info = InterFTRid.objects.get(f_rid=f_rid, t_rid=t_rid, turn_dir_no=turn_dir_no)

        data = {'f_rid': ft_rid_info.f_road_name + ' - ' + str(ft_rid_info.f_angle),
                't_rid': ft_rid_info.t_road_name + ' - ' + str(ft_rid_info.t_angle),
                'turn_dir': turn_dir,
                }

    phase_road_ftrid.save()

    return JsonResponse(data)


# 删除相位进口道rid对应关系数据
def delete_map_ft(request):
    map_id = request.POST.get('map_id', '')

    # 根据map_id确定当前的PhaseFroadFTRidMap
    try:
        phase_road_ftrid = PhaseFroadFTRidMap.objects.get(id=map_id)

        phase_road_ftrid.f_rid_id = None
        phase_road_ftrid.t_rid_id = None
        phase_road_ftrid.turn_dir_no = None

        phase_road_ftrid.save()

        data = {'res': True}
    except Exception as e:
        print(e)
        data = {'res': False}

    return JsonResponse(data)


# 测试
def test(request):
    inter_list = CustSignalInterMap.objects.values('inter_id').distinct()

    for inter_id in inter_list:
        res = save_phase_cust_road(inter_id.get('inter_id'))
        print(inter_id.get('inter_id') + str(res))

    data = {'data': ''}

    return JsonResponse(data)
















