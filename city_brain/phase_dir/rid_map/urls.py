from django.urls import path
from . import views


urlpatterns = [
    path('rid_map/', views.rid_map_show),
    path('get_road_info/', views.get_road_info),
    path('get_rid_info/', views.get_rid_info),
]
