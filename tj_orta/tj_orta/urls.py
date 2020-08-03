"""tj_orta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apscheduler.schedulers.background import BackgroundScheduler
from tj_orta_app.views_sys import forbid_submit, init_sys

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('tj_orta_app.urls')),
]


# 定时任务
Scheduler = BackgroundScheduler()
# 每月25日0点, 禁止提交申请
Scheduler.add_job(forbid_submit, 'cron', day=26, hour=0, minute=0, second=0)
# 每月1日1点, 重置数据库
Scheduler.add_job(init_sys, 'cron', day=29, hour=18, minute=38, second=0)

Scheduler.start()
