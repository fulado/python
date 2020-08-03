from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all_show/?', views.delete_info),
    url(r'^detail_show/?', views.delete_info),
    url(r'^save_info/?', views.delete_info),
    url(r'^delete_info/?', views.delete_info),
]

