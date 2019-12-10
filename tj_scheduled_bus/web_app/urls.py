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
    url(r'^zhidui/vehicle/?', views_zhidui.vehicle),
    url(r'^zhidui/permission/?', views_zhidui.permission),

    # 总队
    url(r'^zongdui/enterprise/?', views_zongdui.enterprise),
    url(r'^zongdui/vehicle/?', views_zongdui.vehicle),
    url(r'^zongdui/station_add/?', views_zongdui.station_add),
    url(r'^zongdui/station/?', views_zongdui.station),

    # 企业端，企业管理
    url(r'^enterprise_add/?', views.enterprise_add),
    url(r'^enterprise_modify/?', views.enterprise_modify),
    url(r'^enterprise_delete/?', views.enterprise_delete),
    url(r'^enterprise_submit/?', views.enterprise_submit),
    url(r'^enterprise/?', views.enterprise),

    # 企业车辆管理
    url(r'^vehicle_add/?', views.vehicle_add),
    url(r'^vehicle_modify/?', views.vehicle_modify),
    url(r'^vehicle_delete/?', views.vehicle_delete),
    url(r'^vehicle_submit/?', views.vehicle_submit),
    url(r'^is_vehicle_exist/?', views.is_vehicle_exist),
    url(r'^vehicle/?', views.vehicle),

    # 企业通行证管理
    url(r'^permission_add/?', views.permission_add),
    url(r'^permission/?', views.permission),

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
    url(r'^check_code/?', views.check_code),
    url(r'^/?', views.login),
]
