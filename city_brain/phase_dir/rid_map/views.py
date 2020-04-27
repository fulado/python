from django.shortcuts import render
from .models import CustFroad, InterRid
from .utils import get_pos2

# Create your views here.


def rid_map_show(request):
    cust_froad_list = CustFroad.objects.all()

    rid_list = InterRid.objects.filter(ft_type_no=1)

    context = {'cust_froad_list': cust_froad_list,
               'rid_list': rid_list,
               }

    return render(request, 'froad_rid.html', context)








