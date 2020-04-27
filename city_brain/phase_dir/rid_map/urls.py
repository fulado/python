from django.urls import path
from . import views


urlpatterns = [
    path('rid_map/', views.rid_map_show),
]
