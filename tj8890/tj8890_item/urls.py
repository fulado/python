from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^create_item/', views.create_item),  # 创建1条事件数据
    url(r'^all/?', views.all_show),
]


