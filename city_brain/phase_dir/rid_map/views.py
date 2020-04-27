from django.shortcuts import render

# Create your views here.


def rid_map_show(request):
    return render(request, 'froad_rid.html')

