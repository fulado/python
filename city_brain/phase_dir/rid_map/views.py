from django.shortcuts import render
from django.http import JsonResponse
from .models import CustFroad, InterRid, RoadRidMap
from .utils import get_pos2

# Create your views here.


def rid_map_show(request):
    cust_froad_list = CustFroad.objects.all()

    rid_list = InterRid.objects.filter(ft_type_no=1)

    map_list = RoadRidMap.objects.all()

    context = {'cust_froad_list': cust_froad_list,
               'rid_list': rid_list,
               'map_list': map_list,
               }

    return render(request, 'froad_rid.html', context)


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

    try:
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

    if road_id != '' and rid_id != '':
        road_rid_map = RoadRidMap()
        road_rid_map.road_id = road_id
        road_rid_map.rid_id = rid_id

        road_rid_map.save()

        map_id = road_rid_map.id
        res = {'map_id': map_id}
    else:
        res = {}

    return JsonResponse(res)


# 删除对应关系
def delete_map(request):
    map_id = request.POST.get('map_id', '')

    try:
        RoadRidMap.objects.get(id=map_id).delete()
    except:
        pass

    res = {}

    return JsonResponse(res)


























