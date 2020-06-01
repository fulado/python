from django.urls import path
from . import views, views_ft


urlpatterns = [
    path('rid_map/', views.rid_map_show),
    path('main/', views.main),
    path('get_road_info/', views.get_road_info),
    path('get_rid_info/', views.get_rid_info),
    path('save_map/', views.save_map),
    path('delete_map/', views.delete_map),
    path('gen_phase_dir/', views.gen_phase_dir),
    path('export_phase_plan_dir/', views.export_phase_plan_dir),
    path('write_phase_dir_data_into_odps/', views.write_phase_dir_data_into_odps),
    path('write_inter_phase_data_into_odps/', views.write_inter_phase_data_into_odps),

    # ft_rid版本
    path('main_ft/', views_ft.main),
    path('rid_map_ft/', views_ft.rid_map_show),
    path('get_t_rid_list/', views_ft.get_t_rid_list),
    path('get_trun_list/', views_ft.get_trun_list),
    path('add_map_ft/', views_ft.add_map_ft),

    # test
    path('test/', views_ft.test),

    path('', views.select),
]
