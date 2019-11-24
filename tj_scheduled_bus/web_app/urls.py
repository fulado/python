from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/?', views.main),
    url(r'^register/?', views.register),
    url(r'^enterprise_info/?', views.enterprise_info),
    url(r'^enterprise/?', views.enterprise),
    url(r'^vehicle/?', views.vehicle),
    url(r'^station/?', views.station),
    url(r'^/?', views.login),
]
