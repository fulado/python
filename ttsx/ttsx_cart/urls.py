from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.add),
    url(r'^cart_count/$', views.cart_count),
    url(r'^cart/$', views.cart),
]
