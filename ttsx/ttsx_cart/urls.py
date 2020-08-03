from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.add),
    url(r'^cart_count/$', views.cart_count),
    url(r'^cart/$', views.cart_show),
    url(r'^modify/$', views.modify),
    url(r'^del_cart/$', views.del_cart),
    url(r'^order/$', views.order),
]
