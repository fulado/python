from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all_show/?', views.all_show),
    url(r'^detail_show/?', views.detail_show),
    url(r'^save_info/?', views.save_info),
    url(r'^delete_info/?', views.delete_info),
]

