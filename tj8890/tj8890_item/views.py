from django.shortcuts import render

# Create your views here.


def all_show(request):
    return render(request, 'item/all.html')
