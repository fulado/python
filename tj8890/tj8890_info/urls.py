from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all_show/?', views.all_show),
    url(r'^detail_show/?', views.detail_show),
]

