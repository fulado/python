from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^create_item/', views.create_item),  # 创建1条事件数据
    url(r'^main/?', views.main_show),
    url(r'^all/?', views.all_show),
    # url(r'^not_deliver/?', views.not_deliver_show),
    url(r'^detail/?', views.detail_show),

    url(r'^deliver_action/?', views.deliver_action),            # 转办
    url(r'^deliver_cancel/?', views.deliver_cancel),            # 撤销转办
    url(r'^remind_item/?', views.remind_item),                  # 催办
    url(r'^return_item/?', views.return_item),                  # 退回重办
    url(r'^save_item/?', views.save_item),                      # 办结保存
    url(r'^delay_approve_item/?', views.delay_approve_item),    # 同意延期
    url(r'^delay_reject_item/?', views.delay_reject_item),      # 驳回延期
    url(r'^delete_item/?', views.delete_item),                  # 驳回延期

    url(r'^accept_item/?', views.accept_item),          # 客户端接受转办事项
    url(r'^reject_item/?', views.reject_item),          # 客户端回驳转办事项
    url(r'^complete_item/?', views.complete_item),      # 客户端办结事项
    url(r'^delay_item/?', views.delay_item),            # 客户端延期申请

    url(r'^import_excel/?', views.import_excel),        # 导入事项数据
    url(r'^export_excel/?', views.export_excel),        # 导出办结事项
    url(r'^cate_search/?', views.cate_search),
    url(r'^over_time_test/?', views.check_dead_time),   # 测试是否超时

    url(r'^item_count/?', views.item_count),   # 获取各类事项总数
    url(r'^cate_add/?', views.cate_add),
    url(r'^cate_modify/?', views.cate_modify),
    url(r'^cate_del/?', views.cate_del),
    url(r'^cate/?', views.cate_show),
]

