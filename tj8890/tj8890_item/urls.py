from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^create_item/', views.create_item),  # 创建1条事件数据
    url(r'^main/?', views.main_show),
    url(r'^all/?', views.all_show),
    # url(r'^not_deliver/?', views.not_deliver_show),
    url(r'^detail/?', views.detail_show),
    url(r'^deliver_action/?', views.deliver_action),    # 转办
    url(r'^deliver_cancel/?', views.deliver_cancel),    # 撤销转办
    url(r'^urge/?', views.urge),  # 催办
    url(r'^cate_search/?', views.cate_search),
]

