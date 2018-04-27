from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from .models import User, Vehicle
from tj_orta.utils import MyPaginator
from .utils import generate_certification
from tj_orta import settings
from .decorator import login_check
import hashlib
import time
import random
import os
import xlrd
from PIL import Image, ImageDraw, ImageFont
import io
# Create your views here.


# 创建超级用户
def create_admin(request):
    user = User()
    user.username = 'admin'
    user.password = hashlib.sha1('yxtc_20921'.encode('utf8')).hexdigest()
    user.authority_id = 99
    try:
        user.save()
    except Exception as e:
        print(e)
        return HttpResponse('创建失败')
    else:
        return HttpResponse('创建成功')


# 验证码
def check_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 23)
    # 构造字体颜色
    fontcolor = (255, 243, 67)
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['check_code'] = rand_str
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    # 内存文件操作
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 显示登录页
def login(request):
    # session中的user_id不等于空直接跳转到主页
    user_id = request.session.get('user_id', '')
    if user_id != '':
        return HttpResponseRedirect('/main')

    msg = request.GET.get('msg', '')

    context = {'msg': msg}

    return render(request, 'login.html', context)


# 登陆服务
def login_handle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('check_code').upper()

    session_code = request.session.get('check_code')

    if code != session_code:
        msg = '验证码错误'
        return HttpResponseRedirect('/?msg=%s' % msg)

    user_list = User.objects.filter(username=username)
    if len(user_list) == 0:
        msg = '用户不存在'
        return HttpResponseRedirect('/?msg=%s' % msg)

    user = user_list[0]
    if hashlib.sha1(password.encode('utf8')).hexdigest() != user.password:
        msg = '用户名或密码错误'
        return HttpResponseRedirect('/?msg=%s' % msg)

    # 把user.id保存到session中
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    request.session['user_id'] = user.id

    return HttpResponseRedirect('/main')


# 退出登录
def logout(request):
    request.session.clear()
    request.session.flush()

    return HttpResponseRedirect('/')


# 显示主页面
@login_check
def main(request):
    user_id = request.session.get('user_id', '')

    if user_id != '':
        user = User.objects.filter(id=user_id)[0]
    # 这里有点问题, user不一定有值, 后面得修改
    context = {'user': user}

    return render(request, 'main.html', context)


# 显示企业管理页面
@login_check
def enterprise(request):
    # 查询企业信息
    enterprise_list = User.objects.filter(is_delete=False).order_by('-id')

    # 获取企业搜索信息
    search_name = request.GET.get('search_name', '')
    # 在结果集中搜索包含搜索信息的企业
    if search_name != '':
        enterprise_list = enterprise_list.filter(enterprise_name__contains=search_name)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(enterprise_list, 10, page_num)

    context = {'mp': mp, 'search_name': search_name}
    
    return render(request, 'enterprise.html', context)


# 添加企业
def enterprise_add(request):
    # 获取企业信息
    username = request.POST.get('username')                 # 帐号
    password = request.POST.get('password')                 # 密码 不能使用'########'
    authority = int(request.POST.get('author'))             # 权限等级
    enterprise_name = request.POST.get('companyName', '')   # 企业名称
    enterprise_phone = request.POST.get('tel', '')          # 企业联系方式
    legal_person = request.POST.get('corName', '')          # 法人
    organization_code = request.POST.get('orgCode', '')     # 组织机构代码
    contact = request.POST.get('contect', '')               # 联系人
    contact_phone = request.POST.get('conMobile', '')       # 联系人电话

    # 创建user
    user = User()
    user.username = username
    user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
    user.authority_id = authority
    user.enterprise_name = enterprise_name
    user.enterprise_phone = enterprise_phone
    user.legal_person = legal_person
    user.organization_code = organization_code
    user.contact = contact
    user.contact_phone = contact_phone

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 判断用户名是否已经存在
def is_user_exist(request):
    username = request.GET.get('username')
    user_id = request.GET.get('id', 0)

    if user_id == 0:
        is_exist = User.objects.filter(username=username).exists()
    else:
        is_exist = User.objects.filter(username=username).exclude(id=user_id).exists()

    return JsonResponse({'is_exist': is_exist})


# 编辑企业信息
def enterprise_modify(request):
    # 获取企业信息
    username = request.POST.get('username')                 # 帐号
    password = request.POST.get('password')                 # 密码
    authority = int(request.POST.get('author'))             # 权限等级
    enterprise_name = request.POST.get('companyName', '')   # 企业名称
    enterprise_phone = request.POST.get('tel', '')          # 企业联系方式
    legal_person = request.POST.get('corName', '')          # 法人
    organization_code = request.POST.get('orgCode', '')     # 组织机构代码
    contact = request.POST.get('contect', '')               # 联系人
    contact_phone = request.POST.get('conMobile', '')       # 联系人电话
    user_id = request.POST.get('id')                        # 用户id

    # 查询用户
    user = User.objects.filter(id=user_id).filter(is_delete=False)[0]

    # 保存user信息
    user.username = username
    user.authority_id = authority
    user.enterprise_name = enterprise_name
    user.enterprise_phone = enterprise_phone
    user.legal_person = legal_person
    user.organization_code = organization_code
    user.contact = contact
    user.contact_phone = contact_phone
    # 如果密码不能8个'#', 需要修改密码
    if password != r'########':
        user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
        print('change password')

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 删除用户信息
def enterprise_delete(request):
    # 获取用户id
    user_id = request.POST.get('id')  # 用户id

    # 查询user
    user = User.objects.filter(id=user_id).filter(is_delete=False)[0]

    # 删除user
    try:
        user.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 显示车辆管理页面
@login_check
def vehicle(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        vehicle_list = Vehicle.objects.filter(enterprise_id=user_id).order_by('-modify_time')
    else:
        vehicle_list = Vehicle.objects.all().order_by('-modify_time')

    # 获取车辆搜索信息
    search_name = request.GET.get('search_name', '')

    # 在结果集中搜索包含搜索信息的车辆, 车辆搜索功能不完善, 指数如车牌号,不要输入号牌所在地
    if search_name != '':
        vehicle_list = vehicle_list.filter(number__contains=search_name)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp, 'search_name': search_name}

    return render(request, 'vehicle.html', context)


# 显示审核页面
def verify(request):
    return render(request, 'verify.html')


# 添加车辆
def vehicle_add(request):
    # 获取用户提交的车辆信息
    # location_id = int(request.GET.get('location'))          # 车牌所在地
    number = request.GET.get('number')                      # 号牌号码
    engine = request.GET.get('engine')                      # 发动机型号
    vehicle_type_id = int(request.GET.get('vehicle_type'))     # 车辆类型
    vehicle_model = request.GET.get('vehicle_model')        # 车辆型号
    register_date = request.GET.get('register_date')        # 车辆注册日期
    route = request.GET.get('route')                        # 路线

    # 创建车辆数据对象
    truck = Vehicle()
    truck.vehicle_type_id = vehicle_type_id
    # truck.location_id = location_id
    truck.number = number
    truck.engine = engine
    truck.vehicle_model = vehicle_model
    truck.register_date = register_date
    truck.route = route
    truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        truck.enterprise_id = user_id
    else:
        truck.enterprise_id = 1

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 编辑车辆
def vehicle_modify(request):
    # 获取用户提交的车辆信息
    # location_id = int(request.GET.get('location'))          # 车牌所在地
    number = request.GET.get('number')                      # 号牌号码
    engine = request.GET.get('engine')                      # 发动机型号
    vehicle_type_id = int(request.GET.get('vehicle_type'))  # 车辆类型
    vehicle_model = request.GET.get('vehicle_model')        # 车辆型号
    register_date = request.GET.get('register_date')        # 车辆注册日期
    route = request.GET.get('route')                        # 路线
    vehicle_id = request.GET.get('vehicle_id')              # id

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]
    truck.vehicle_type_id = vehicle_type_id
    # truck.location_id = location_id
    truck.number = number
    truck.engine = engine
    truck.vehicle_model = vehicle_model
    truck.register_date = register_date
    truck.route = route
    truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 审核状态变为未提交
    truck.status_id = 1

    # 删除原有的通行证图片文件
    file_name = truck.file_name

    if file_name is not None and file_name != '':
        file_name = r'%s/certification/%s' % (settings.FILE_DIR, file_name)
        truck.file_name = None
        truck.cert_id = None
        if os.path.exists(file_name):
            os.remove(file_name)

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 删除车辆
def vehicle_delete(request):
    # 获取车辆id
    vehicle_id = request.GET.get('vehicle_id')  # 车辆i

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]

    # 删除车辆
    try:
        truck.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 提交车辆
def vehicle_submit(request):
    vehicle_id = request.GET.get('vehicle_id')  # id

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]

    # 审核状态变为通过
    truck.status_id = 4

    # 生成通行证图片
    # 生成通行证id, 201805+车牌号+三位随机数
    # certification_id = '%s%s%d%d%d' % (time.strftime('%Y%m', time.localtime()), truck.number[1:], random.randint(0, 9),
    #                                    random.randint(0, 9), random.randint(0, 9))
    # 临时设定, 记得改掉
    certification_id = '%s%s%d%d%d' % ('201805', truck.number[1:], random.randint(0, 9), random.randint(0, 9),
                                       random.randint(0, 9))

    truck.cert_id = certification_id
    limit_data = '2018年5月31日'  # 暂时写为5月底
    number = '%s' % truck.number
    enterprise_name = truck.enterprise.enterprise_name
    route = truck.route
    # 图片文件名
    file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
    truck.file_name = '%s.jpg' % certification_id

    generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 批量导入车辆信息
def excel_import(request):
    # 获取用户上传的excel文件, 文件不存储, 在内存中对文件进行操作
    excel_file = request.FILES.get('excel_file')

    # 打开excel文件, 直接从内存读取文件内容
    workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
    # 获得sheets列表
    sheets = workbook.sheet_names()
    # 获得第一个sheet对象
    worksheet = workbook.sheet_by_name(sheets[0])
    # 遍历
    new_truck_list = []
    for i in range(1, worksheet.nrows):
        # row = worksheet.row(i)
        # 读取一条车辆信息
        vehicle_type = worksheet.cell_value(i, 1)           # 车辆类型

        if worksheet.cell(i, 2).ctype == 2:
            number = str(int(worksheet.cell_value(i, 2)))       # 车牌号
        else:
            number = str(worksheet.cell_value(i, 2))

        if worksheet.cell(i, 3).ctype == 2:
            engine = str(int(worksheet.cell_value(i, 3)))       # 发动机型号
        else:
            engine = str(worksheet.cell_value(i, 3))

        vehicle_model = str(worksheet.cell_value(i, 4))         # 车辆型号
        register_date = str(worksheet.cell_value(i, 5))           # 注册日期
        route = str(worksheet.cell_value(i, 6))                   # 路线

        # print('%s %s %s %s %s %s' % (vehicle_type, number, engine, vehicle_model, register_date, route))
        # 如果车牌不为空, 创建车辆对象, 否则略过该条数据
        is_exist = False
        if number == '' or number is None:
            is_exist = True

        if not is_exist:
            # 如果库中已经存在该车牌, 则忽略该车辆, 否者创建新的车辆对象
            # 获取session中的user_id, 根据user_id查询企业
            user_id = int(request.session.get('user_id', ''))

            # 查询该企业的所有车辆数据
            if user_id == '' or user_id == 1:
                is_exist = True
            else:
                is_exist = Vehicle.objects.filter(enterprise_id=user_id).filter(number=number).exists()

        if not is_exist:
            truck = Vehicle()
            truck.number = number

            # 添加车辆属性
            if vehicle_type != '' and vehicle_type is not None:
                if vehicle_type == '大型货车':
                    truck.vehicle_type_id = 1
                elif vehicle_type == '小型货车':
                    truck.vehicle_type_id = 2
                elif vehicle_type == '挂式货车':
                    truck.vehicle_type_id = 15

            if engine != '' and engine is not None:
                truck.engine = engine

            if vehicle_model != '' and vehicle_model is not None:
                truck.vehicle_model = vehicle_model

            # 车辆注册日期, 应该判断一下格式是否正确, 不正确添加默认值, 或设置为空, 现在没时间做了
            if register_date != '' and register_date is not None:
                truck.register_date = register_date

            if route != '' and route is not None:
                truck.route = route

            truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            if user_id != '' and user_id != 1:
                truck.enterprise_id = user_id
            else:
                truck.enterprise_id = 1     # 多此一举

            new_truck_list.append(truck)
            #truck.save()

    Vehicle.objects.bulk_create(new_truck_list)

        # for j in range(1, worksheet.ncols):
            # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error
            # 判断数据的类型, 如果是数字, 默认显示为浮点数, 这里转成整数
            # if worksheet.cell(i, j).ctype == 2:
            #     print("%s\t" % int(worksheet.cell_value(i, j)), end="")
            # else:
            #     print("%s\t" % worksheet.cell_value(i, j), end="")

    return HttpResponseRedirect('/vehicle')


# 提交全部车辆(request):
def vehicle_submit_all(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        truck_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1)

    # 判断查询结果集是否为空
    if len(truck_list) > 0:
        for truck in truck_list:
            # 审核状态变为通过
            truck.status_id = 4

            # 生成通行证图片
            # 生成通行证id, 201805+车牌号+三位随机数
            certification_id = '%s%s%d%d%d' % (time.strftime('%Y%m', time.localtime()), truck.number[1:],
                                               random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
            truck.cert_id = certification_id
            limit_data = '2018年5月31日'  # 暂时写为5月底
            number = '%s' % truck.number
            enterprise_name = truck.enterprise.enterprise_name
            route = truck.route
            # 图片文件名
            file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
            truck.file_name = '%s.jpg' % certification_id

            generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)

            # 存入数据库
            try:
                truck.save()
            except Exception as e:
                print(e)

    return HttpResponseRedirect('/vehicle')


# 显示通行证查询下载页面
def download(request):
    # 获取车牌号
    number = request.GET.get('number', '')

    status = 99
    truck = None
    # 如果number为空, 当前是未查询状态
    if number != '':
        # 通过车牌查询车辆
        truck_list = Vehicle.objects.filter(number=number)

        if len(truck_list) > 0:
            truck = truck_list[0]
            status = truck.status_id
        else:
            status = 0   # 车辆不存在

    context = {'status': status, 'truck': truck, 'number': number}

    return render(request, 'download.html', context)


# 通行证查询
def download_search(request):
    # 获取车牌号
    number = request.GET.get('number', '')

    return HttpResponseRedirect('/download?number=%s' % number)


# 生成密码
# def generate_pwd(reqeust):
#     user_list = User.objects.all()
#
#     for user in user_list:
#         password = hashlib.sha1(user.password.encode('utf8')).hexdigest()
#         user.password = password
#
#         user.save()
#
#     return HttpResponse('创建成功')
