from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^create_admin/?', views.create_admin),  # 创建管理员帐号, 不要轻易使用
    url(r'^main/?', views.main),
    url(r'^enterprise_add/?', views.enterprise_add),
    url(r'^enterprise_modify/?', views.enterprise_modify),
    url(r'^enterprise_delete/?', views.enterprise_delete),
    url(r'^enterprise/?', views.enterprise),
    url(r'^vehicle_add/?', views.vehicle_add),
    url(r'^vehicle_modify/?', views.vehicle_modify),
    url(r'^vehicle_delete/?', views.vehicle_delete),
    url(r'^vehicle_submit_all/?', views.vehicle_submit_all),
    url(r'^vehicle_submit/?', views.vehicle_submit),
    url(r'^vehicle/?', views.vehicle),
    url(r'^verify_pass/?', views.verify_pass),                  # 车辆审核通过
    url(r'^verify_refuse/?', views.verify_refuse),              # 车辆审核不通过
    url(r'^verify/?', views.verify),                            # 显示车辆审核页面
    url(r'^excel_import/?', views.excel_import),
    url(r'^is_user_exist/?', views.is_user_exist),
    url(r'^check_code/?', views.check_code),
    url(r'^login_handle/?', views.login_handle),
    url(r'^logout/?', views.logout),
    url(r'^download_search/?', views.download_search),
    url(r'^download/?', views.download),
    url(r'^is_reach_limit/?', views.is_reach_limit),            # 判断是否到达车辆提交上限
    url(r'^can_submit_all/?', views.can_submit_all),            # 判断是否可以提交全部车辆
    url(r'^export_xls/?', views.export_xls),                    # 导出待审核车辆
    url(r'^import_xls/?', views.import_xls),                    # 导入审核后的车辆数据
    # url(r'^generate_pwd/?', views.generate_pwd),
    url(r'^my_test/?', views.my_test),                          # 测试用
    url(r'^/?', views.login),
]
