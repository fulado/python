from django.urls import path
from . import views


urlpatterns = [
    path('rid_map/', views.rid_map_show),
    path('main/', views.main),
    path('get_road_info/', views.get_road_info),
    path('get_rid_info/', views.get_rid_info),
    path('save_map/', views.save_map),
    path('delete_map/', views.delete_map),
    # path('test_phase/', views.test_phase),
    path('', views.select),
]
