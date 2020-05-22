from django.urls import path
from . import views


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
    path('', views.select),
]
