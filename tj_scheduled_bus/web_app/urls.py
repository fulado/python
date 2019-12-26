from django.conf.urls import url
from . import views
from . import views_zhidui
from . import views_zongdui


urlpatterns = [
    # 支队
    url(r'^zhidui/enterprise_refuse/?', views_zhidui.enterprise_refuse),
    url(r'^zhidui/enterprise_pass/?', views_zhidui.enterprise_pass),
    url(r'^zhidui/enterprise/?', views_zhidui.enterprise),
    url(r'^zhidui/vehicle_refuse/?', views_zhidui.vehicle_refuse),
    url(r'^zhidui/vehicle_pass/?', views_zhidui.vehicle_pass),
    url(r'^zhidui/vehicle_mark_show/?', views_zhidui.vehicle_mark_show),
    url(r'^zhidui/vehicle_mark/?', views_zhidui.vehicle_mark),
    url(r'^zhidui/vehicle_unlock/?', views_zhidui.vehicle_unlock),
    url(r'^zhidui/vehicle/?', views_zhidui.vehicle),
    url(r'^zhidui/permission/?', views_zhidui.permission),
    url(r'^zhidui/department_modify/?', views_zhidui.department_modify),
    url(r'^zhidui/department/?', views_zhidui.department),
    url(r'^zhidui/mark_delete/?', views_zhidui.mark_delete),
    url(r'^zhidui/mark/?', views_zhidui.mark),

    # 总队
    url(r'^zongdui/enterprise/?', views_zongdui.enterprise),
    url(r'^zongdui/vehicle/?', views_zongdui.vehicle),
    url(r'^zongdui/station_add/?', views_zongdui.station_add),
    url(r'^zongdui/station_modify/?', views_zongdui.station_modify),
    url(r'^zongdui/station_delete/?', views_zongdui.station_delete),
    url(r'^zongdui/station/?', views_zongdui.station),
    url(r'^zongdui/can_add_account/?', views_zongdui.can_add_account),
    url(r'^zongdui/account_add/?', views_zongdui.account_add),
    url(r'^zongdui/account_modify/?', views_zongdui.account_modify),
    url(r'^zongdui/account_delete/?', views_zongdui.account_delete),
    url(r'^zongdui/account_lock/?', views_zongdui.account_lock),
    url(r'^zongdui/account_unlock/?', views_zongdui.account_unlock),
    url(r'^zongdui/account/?', views_zongdui.account),

    # 企业端，企业管理
    url(r'^enterprise_add/?', views.enterprise_add),
    url(r'^enterprise_modify/?', views.enterprise_modify),
    url(r'^enterprise_delete/?', views.enterprise_delete),
    url(r'^enterprise_submit/?', views.enterprise_submit),
    url(r'^is_enterprise_exist/?', views.is_enterprise_exist),
    url(r'^is_own_enterprise_exist/?', views.is_own_enterprise_exist),
    url(r'^enterprise/?', views.enterprise),

    # 企业车辆管理
    url(r'^vehicle_add/?', views.vehicle_add),
    url(r'^vehicle_modify/?', views.vehicle_modify),
    url(r'^vehicle_delete/?', views.vehicle_delete),
    url(r'^vehicle_submit/?', views.vehicle_submit),
    url(r'^vehicle_unlock/?', views.vehicle_unlock),
    url(r'^can_add_vehicle/?', views.can_add_vehicle),
    url(r'^vehicle/?', views.vehicle),
    url(r'^mark/?', views.mark),

    # 企业通行证管理
    url(r'^permission_add/?', views.permission_add),
    url(r'^permission/?', views.permission),
    url(r'^is_vehicle_expired/?', views.is_vehicle_expired),
    url(r'^download_count/?', views.download_count),

    # 企业路线管理
    url(r'^station_search/?', views.station_search),
    url(r'^station_add/?', views.station_add),
    url(r'^station_delete/?', views.station_delete),
    url(r'^station_cancel/?', views.station_cancel),
    url(r'^station_save/?', views.station_save),
    url(r'^station/?', views.station),
    url(r'^can_add_station/?', views.can_add_station),

    # 公用
    url(r'^main/?', views.main),
    url(r'^register_handle/?', views.register_handle),
    url(r'^register/?', views.register),
    url(r'^login_handle/?', views.login_handle),
    url(r'^login/?', views.login),
    url(r'^logout/?', views.logout),
    url(r'^change_password/?', views.change_password),
    url(r'^password_modify/?', views.password_modify),
    url(r'^password/?', views.password),
    url(r'^sms_check_code/?', views.sms_check_code),
    url(r'^check_code/?', views.check_code),
    url(r'^/?', views.login),
]
