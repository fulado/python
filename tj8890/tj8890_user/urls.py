from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^create_admin/', views.create_admin),  # 创建管理员帐号, 不要轻易使用
    url(r'^login/?', views.login_service),
    url(r'^logout/?', views.logout),
    url(r'^dept_add/?', views.dept_add),
    url(r'^dept_modify/?', views.dept_modify),
    url(r'^dept_del/?', views.dept_del),
    url(r'^dept_search/?', views.dept_search),
    url(r'^dept/?', views.dept_show),
    url(r'^user_add/?', views.user_add),
    url(r'^user_modify/?', views.user_modify),
    url(r'^user_del/?', views.user_del),
    url(r'^reset_password/?', views.reset_password),
    url(r'^user/?', views.user_show),
    url(r'^', views.login),
]


