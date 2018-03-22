from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$', views.login_service),
]


