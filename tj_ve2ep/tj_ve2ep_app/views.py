from django.shortcuts import render
from django.http import HttpResponse
from .models import TbCarData
import xlrd
import datetime

# Create your views here.


# just for test
def test(request):
    truck_count = TbCarData.objects.all().count()

    print(truck_count)

    return HttpResponse('Ok')


# 导入数据页面
def show_import(request):
    return render(request, 'main.html')


# 导入excel数据到oracle数据库
def import_xls(request):
    # 获取用户上传的excel文件, 文件不存储, 在内存中对文件进行操作
    excel_file = request.FILES.get('excel_file')

    # 打开excel文件, 直接从内存读取文件内容
    workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
    # 获得sheets列表
    sheets = workbook.sheet_names()
    # 获得第一个sheet对象
    worksheet = workbook.sheet_by_name(sheets[0])

    # 存储车辆信息的列表
    vehicle_list = []
    # 遍历
    for i in range(1, worksheet.nrows):
        # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error

        # 读取车辆id
        if worksheet.cell(i, 0).ctype != 5 and worksheet.cell_value(i, 0) != '':
            vehicle_id = worksheet.cell_value(i, 0)
        else:
            continue

        # 读取号牌号码
        if worksheet.cell(i, 1).ctype != 5 and worksheet.cell_value(i, 1) != '':
            hphm = worksheet.cell_value(i, 1)
        else:
            continue

        # 读取号牌种类
        if worksheet.cell(i, 2).ctype != 5 and worksheet.cell_value(i, 2) != '':
            hpzl = worksheet.cell_value(i, 2)
        else:
            continue

        # 读取违法代码
        if worksheet.cell(i, 3).ctype != 5 and worksheet.cell_value(i, 3) != '':
            wfdm = worksheet.cell_value(i, 3)
        else:
            continue

        # 读取起始时间
        if worksheet.cell(i, 4).ctype == 3:
            qssj = xlrd.xldate_as_datetime(worksheet.cell_value(i, 4), 0)
            # qssj = datetime.datetime.strftime(qssj, r'%Y-%m-%d %H:%M:%S')
        elif worksheet.cell(i, 4).ctype != 5 and worksheet.cell_value(i, 1) != '':
            qssj = worksheet.cell_value(i, 4)
        else:
            continue

        # 读取截至时间
        if worksheet.cell(i, 5).ctype == 3:
            jzsj = xlrd.xldate_as_datetime(worksheet.cell_value(i, 5), 0)
            # jzsj = datetime.datetime.strftime(jzsj, r'%Y-%m-%d %H:%M:%S')
        elif worksheet.cell(i, 5).ctype != 5 and worksheet.cell_value(i, 1) != '':
            jzsj = worksheet.cell_value(i, 5)
        else:
            continue

        # 计算插入时间和更新时间
        # gxsj = datetime.datetime.strftime(datetime.datetime.now(), r'%Y-%m-%d %H:%M:%S')
        gxsj = datetime.datetime.now()

        vehicle_info = {'id': vehicle_id, 'hphm': hphm, 'hpzl': hpzl, 'wfdm': wfdm, 'qssj': qssj, 'jzsj': jzsj,
                        'gxsj': gxsj}
        vehicle_list.append(vehicle_info)

        # print(qssj)
        # print(jzsj)
        # print(gxsj)

    # 查询车辆更新集合
    vehicle_query_set = TbCarData.objects.filter(wfdm=vehicle_list[0]['wfdm'])

    # 插入车辆集合
    vehicle_inert_list = []

    # 更新到oracle数据库
    for vehicle in vehicle_list:
        vehicle_oracle = vehicle_query_set.filter(hphm=vehicle['hphm'])

        # 如何车辆已经存在, 则更新
        if vehicle_oracle:
            vehicle_oracle = vehicle_oracle[0]
            vehicle_oracle.qssj = vehicle['qssj']
            vehicle_oracle.jzsj = vehicle['jzsj']
            vehicle_oracle.gxsj = vehicle['gxsj']
            vehicle_oracle.save()
        # 如何车辆不存在, 则创建新的车辆
        else:
            vehicle_oracle = TbCarData()
            vehicle_oracle.id = vehicle['id']
            vehicle_oracle.hphm = vehicle['hphm']
            vehicle_oracle.hpzl = vehicle['hpzl']
            vehicle_oracle.wfdm = vehicle['wfdm']
            vehicle_oracle.qssj = vehicle['qssj']
            vehicle_oracle.jzsj = vehicle['jzsj']
            vehicle_oracle.crsj = vehicle['gxsj']
            vehicle_oracle.gxsj = vehicle['gxsj']

            vehicle_inert_list.append(vehicle_oracle)

    if vehicle_inert_list:
        TbCarData.objects.bulk_create(vehicle_inert_list)

    return HttpResponse('<h1>导入完成</h1>')
