from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import Item, Category


# 创建n条事件数据
def create_item(request):
    for i in range(2, 35):
        item = Item()
        item.id = '20170411000' + str(i)
        item.title = '驾驶证丢失'
        item.summary = '''市民来电：2014年4月份违章，但是当时车辆和驾驶证被红桥支队扣下了，现在市民多个途径寻找驾驶证，但均未找到。
        处理当时的违法需要驾驶证，如果撤销不了违法信息接受处罚就不能换本或者是重新学驾驶证。张继德，120224198310131715，津GQ3901。
        现在市民咨询，这种情况该怎么办？'''
        item.order_id = 'GD2016122113557102'
        item.source = '电话语音'
        item.sh_phone = '18622940896'
        item.sh_person = '张先生'
        item.area = '和平区'
        item.recoder = '李申'
        item.recd_time = '2016-12-21 15:49:20'

        item.save()

    return HttpResponse('创建成功')


# 显示全部事项页面
def all_show(request):
    title = ['办理事项管理', '全部事项']
    cate1_list = Category.objects.filter(level=1)
    cate2_list = Category.objects.filter(level=2)
    context = {'title': title, 'cate1_list': cate1_list, 'cate2_list': cate2_list}
    return render(request, 'item/all.html', context)
