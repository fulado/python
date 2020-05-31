from django.shortcuts import render
from django.http import JsonResponse
from .models import CustSignalInterMap, CustFroad, InterRid, InterOutRid, RoadFTRidMap, InterFTRid
from .views import get_cust_phase


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
    ft_f_rid_list = InterFTRid.objects.filter(inter_id=inter_id).values('f_road_name', 'f_angle').distinct()

    if rid_type:
        f_rid_list = f_rid_list.filter(rid_type_no=rid_type)
        t_rid_list = t_rid_list.filter(rid_type_no=rid_type)

    # 获取电科相位方向数据
    cust_phase_dir_list = get_cust_phase(cust_signal_id)

    context = {'cust_froad_list': cust_froad_list,
               'f_rid_list': f_rid_list,
               't_rid_list': t_rid_list,
               'map_list': map_list,
               'inter_id': inter_id,
               'inter_name': inter_map_info.inter_name,
               'cust_signal_id': cust_signal_id,
               'rid_type': rid_type,
               'cust_phase_dir_list': cust_phase_dir_list,
               # 'ft_rid_list': ft_rid_list,
               'ft_f_rid_list': ft_f_rid_list,
               }

    response = render(request, 'froad_rid_ft.html', context)
    response.__setitem__('X-Frame-Options', 'ALLOW-FROM')

    return response


# 获取ft_rid中的出口道rid
def get_t_rid_list(request):
    f_rid_name_angle = request.POST.get('f_rid_name_angle', '')
    f_road_name, f_angle = f_rid_name_angle.split('-')

    ft_t_rid_list = InterFTRid.objects.filter(f_road_name=f_road_name, f_angle=f_angle).\
        values('t_road_name', 't_angle').distinct()

    rid_list = []
    for t_rid in ft_t_rid_list:
        rid = {'t_rid_name_angle': t_rid.get('t_road_name') + '-' + str(t_rid.get('t_angle'))}
        rid_list.append(rid)

    data = {'ft_t_rid_list': rid_list}

    return JsonResponse(data)


# 获取转向列表
def get_trun_list(request):
    f_rid_name_angle = request.POST.get('f_rid_name_angle', '')
    t_rid_name_angle = request.POST.get('t_rid_name_angle', '')
    f_road_name, f_angle = f_rid_name_angle.split('-')
    t_road_name, t_angle = t_rid_name_angle.split('-')

    ft_rid_list = InterFTRid.objects.filter(f_road_name=f_road_name, f_angle=f_angle, t_road_name=t_road_name,
                                            t_angle=t_angle)

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

        data = {'ft_rid_id': ft_rid.id, 'trun_dir': turn_dir}
    else:
        data = {'id': 0, 'trun_dir': '错误'}

    return JsonResponse(data)





















