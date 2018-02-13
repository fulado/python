from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.show_list),
    url(r'^detail/$', views.show_detail),
]

