from django.shortcuts import render

# Create your views here.


# 显示登录页
def login(request):
    return render(request, 'user/login.html')
