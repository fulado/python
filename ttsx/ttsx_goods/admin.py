from django.contrib import admin
from .models import TypeInfo, GoodsInfo

# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title', 'price', 'describe', 'stored']


class TypeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title', 'is_delete']


admin.site.register(TypeInfo, TypeAdmin)
admin.site.register(GoodsInfo, GoodsAdmin)
