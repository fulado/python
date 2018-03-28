from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^create_admin/', views.create_admin),  # 创建管理员帐号, 不要轻易使用
    url(r'^login/?', views.login_service),
    url(r'^dept/?', views.dept),
    url(r'^', views.login),
]

