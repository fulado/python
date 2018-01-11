from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^register/$', views.show_reg),
    url(r'^user_register/$', views.user_register),
    url(r'^login/$', views.show_login),
]
