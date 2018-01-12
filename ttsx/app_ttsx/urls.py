from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^/?$', views.show_index),
    url(r'^index/$', views.show_index),
    url(r'^register/$', views.show_reg),
    url(r'^register_service/$', views.register_service),
    url(r'^login/$', views.show_login),
    url(r'^login_server/$', views.login_server),
]

