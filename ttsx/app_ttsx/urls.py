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
    url(r'^user_site/$', views.show_user_site),
    url(r'^modify_site/$', views.modify_user_site),
    url(r'^user_info/$', views.show_user_info),
    url(r'^logout/$', views.logout),
]

