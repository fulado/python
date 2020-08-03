from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.show_list),
    url(r'^goods_(\d+)/$', views.show_detail),
]

