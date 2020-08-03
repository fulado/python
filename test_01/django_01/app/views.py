from django.shortcuts import HttpResponse

# Create your views here.


def violation(request):
    return HttpResponse('<h1>server_01</h1>')
