from django.shortcuts import render
from .models import CustSignalInterMap, CustFroad, InterRid, InterOutRid, RoadFTRidMap
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
               }

    response = render(request, 'froad_rid_ft.html', context)
    response.__setitem__('X-Frame-Options', 'ALLOW-FROM')

    return response































