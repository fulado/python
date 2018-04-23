from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^create_admin/', views.create_admin),  # 创建管理员帐号, 不要轻易使用
    url(r'^main/?', views.main),
    url(r'^enterprise_add/?', views.enterprise_add),
    url(r'^enterprise_modify/?', views.enterprise_modify),
    url(r'^enterprise_delete/?', views.enterprise_delete),
    url(r'^enterprise/?', views.enterprise),
    url(r'^vehicle_add/?', views.vehicle_add),
    url(r'^vehicle_modify/?', views.vehicle_modify),
    url(r'^vehicle_delete/?', views.vehicle_delete),
    url(r'^vehicle/?', views.vehicle),
    url(r'^verify/?', views.verify),
    url(r'^is_user_exist/?', views.is_user_exist),
]
