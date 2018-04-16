from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^create_item/', views.create_item),  # 创建1条事件数据
    url(r'^all/?', views.all_show),
    url(r'^not_deliver_detail/?', views.not_deliver_detail),
    url(r'^cate_search/?', views.cate_search),
]

