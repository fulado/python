from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^create_admin/', views.create_admin),  # 创建管理员帐号, 不要轻易使用
    url(r'^main/?', views.main),
    url(r'^enterprise_add/?', views.enterprise_add),
    url(r'^enterprise/?', views.enterprise),
]


