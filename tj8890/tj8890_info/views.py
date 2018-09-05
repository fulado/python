from django.shortcuts import render, HttpResponseRedirect
# from tj8890_item.models import Cate
from .models import Information
# from tj8890.utils import MyPaginator
#
# import time
# from tj8890.decorator import login_check
#
# # Create your views here.
#
#
# # 显示所有知识页面
# @login_check
# def all_show(request):
#     title = ['知识库管理', '内容查询']
#
#     # 获得查询知识提交的信息
#     cate1 = int(request.GET.get('cate1', 0))
#     cate2 = int(request.GET.get('cate2', 0))
#     cate3 = int(request.GET.get('cate3', 0))
#     cate4 = int(request.GET.get('cate4', 0))
#     recd_time_begin = request.GET.get('recd_time_begin', '0')
#     recd_time_end = request.GET.get('recd_time_end', '0')
#     keyword = request.GET.get('keyword', '')
#
#     if recd_time_begin == '0':
#         recd_time_begin = time.strftime('%Y-01-01', time.localtime())
#     if recd_time_end == '0':
#         recd_time_end = time.strftime('%Y-%m-%d', time.localtime())
#
#     recd_time_end_research = '%s 23:59:59' % recd_time_end
#
#     # 将检索信息保存到session
#     request.session['cate1'] = cate1
#     request.session['cate2'] = cate2
#     request.session['cate3'] = cate3
#     request.session['cate4'] = cate4
#     request.session['recd_time_begin'] = recd_time_begin
#     request.session['recd_time_end'] = recd_time_end
#     request.session['keyword'] = keyword
#
#     # 事项分类
#     cate1_list = Category.objects.filter(level=1)
#     cate2_list = Category.objects.filter(level=2)
#     cate3_list = Category.objects.filter(cate_id=cate2)
#     cate4_list = Category.objects.filter(cate_id=cate3)
#
#     # 查询事项全部知识
#     info_list = Information.objects.all().order_by('-upload_time')
#
#     # 按照表单中的的信息进行过滤
#     info_list = info_list.filter(upload_time__gte=recd_time_begin)
#     info_list = info_list.filter(upload_time__lte=recd_time_end_research)
#
#     if cate1 != 0:
#         info_list = info_list.filter(category1_id=cate1)
#     if cate2 != 0:
#         info_list = info_list.filter(category2_id=cate2)
#     if cate3 != 0:
#         info_list = info_list.filter(category3_id=cate3)
#     if cate4 != 0:
#         info_list = info_list.filter(category4_id=cate4)
#
#     # 获得用户指定的页面
#     page_num = int(request.GET.get('page_num', 1))
#     # 分页
#     mp = MyPaginator()
#     mp.paginate(info_list, 10, page_num)
#
#     context = {'mp': mp,
#                'cate1_list': cate1_list,
#                'cate2_list': cate2_list,
#                'cate3_list': cate3_list,
#                'cate4_list': cate4_list,
#                'title': title,
#                }
#
#     return render(request, 'info/all.html', context)
#
#
# # 显示知识详情页面
# @login_check
# def detail_show(request):
#     title = ['知识库管理', '添加内容']
#
#     info_id = int(request.GET.get('id', 0))
#     can_save = int(request.GET.get('add', 0))
#     can_delete = int(request.GET.get('delete', 0))
#
#     if info_id == 0:
#         info_id = 1
#
#     info = Information.objects.get(id=info_id)
#
#     # 事项分类
#     cate1_list = Category.objects.filter(level=1)
#     cate2_list = Category.objects.filter(level=2)
#     cate3_list = Category.objects.filter(cate_id=0)
#     cate4_list = Category.objects.filter(cate_id=0)
#
#     context = {'info': info,
#                'can_save': can_save,
#                'can_delete': can_delete,
#                'cate1_list': cate1_list,
#                'cate2_list': cate2_list,
#                'cate3_list': cate3_list,
#                'cate4_list': cate4_list,
#                'title': title,
#                }
#
#     return render(request, 'info/detail.html', context)
#
#
# # 保存知识
# def save_info(request):
#     info_name = request.GET.get('info_name', '')
#     info_abstract = request.GET.get('info_abstract', '')
#     info_content = request.GET.get('info_content', '')
#     # cate1 = int(request.GET.get('cate1', ''))
#     # cate2 = int(request.GET.get('cate2', ''))
#     # cate3 = int(request.GET.get('cate3', ''))
#     # cate4 = int(request.GET.get('cate4', ''))
#
#     user_id = request.session.get('user_id', 1)
#
#     info = Information()
#     info.info_name = info_name
#     info.info_abstract = info_abstract
#     info.info_content = info_content
#     # info.cate1_id = cate1
#     # info.cate2_id = cate2
#     # info.cate3_id = cate3
#     # info.cate4_id = cate4
#     info.upload_user_id = user_id
#     info.upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#
#     try:
#         info.save()
#     except Exception as e:
#         print(e)
#
#     return HttpResponseRedirect('/info/all_show')
#
#
# 删除知识
def delete_info(request):
    info_id = int(request.GET.get('id', 0))

    Information.objects.filter(id=info_id).delete()

    return HttpResponseRedirect('/info/all_show')
