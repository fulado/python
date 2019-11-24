from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.http import FileResponse
from .models import User, Vehicle, VehicleMan
from tj_orta.utils import MyPaginator
from .utils import verify_vehicle, verify_vehicle_pass, generate_certification
from tj_orta import settings
from .decorator import login_check
import hashlib
import time
import random
import xlrd
import xlwt
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
    str1 = 'ABCD23EFGHJK456LMNPQRS789TUVWXYZ'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 设置字体
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 23)
    # 字体颜色
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

    # 根据user.id获取用户权限, 2-环保局, 3-交管局
    if user.id != 0:
        authority = User.objects.get(id=user.id).authority.id
    else:
        authority = 0

    # 把user.id保存到session中
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    request.session['user_id'] = user.id
    request.session['authority_id'] = authority

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
    enterprise_list = User.objects.filter(is_delete=False).exclude(id=1).order_by('id')

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

    # 保存当前页面状态到session
    request.session['search_name'] = search_name
    request.session['page_num'] = page_num

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
    limit_number = request.POST.get('limit_number', '1')    # 申请通行证上限
    if limit_number is not None:
        if limit_number.isdigit():
            limit_number = int(limit_number)
        else:
            limit_number = 1

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
    user.limit_number = limit_number

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    # 构建返回url
    search_name = request.session.get('search_name', '')
    page_num = request.session.get('page_num', '')

    url = '/enterprise?search_name=%s&page_num=%s' % (search_name, page_num)

    return HttpResponseRedirect(url)


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
    limit_number = request.POST.get('limit_number', '1')  # 申请通行证上限
    if limit_number is not None:
        if limit_number.isdigit():
            limit_number = int(limit_number)
        else:
            limit_number = 1

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
    user.limit_number = limit_number
    # 如果密码不能8个'#', 需要修改密码
    if password != r'########':
        user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
        print('change password')

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    # 构建返回url
    search_name = request.session.get('search_name', '')
    page_num = request.session.get('page_num', '')
    url = '/enterprise?search_name=%s&page_num=%s' % (search_name, page_num)

    return HttpResponseRedirect(url)


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

    # 构建返回url
    search_name = request.session.get('search_name', '')
    page_num = request.session.get('page_num', '')
    url = '/enterprise?search_name=%s&page_num=%s' % (search_name, page_num)

    return HttpResponseRedirect(url)


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


# 显示审核页面
@login_check
def verify(request):

    # 获取查询信息
    number = request.GET.get('number', '')

    # 根据用户提交的查询信息, 查询车辆数据
    if number == '':
        # 如果未输入车牌号, 默认查询全部车辆, 未提交申请车辆除外
        vehicle_list = Vehicle.objects.all().exclude(status_id=1)
    else:
        vehicle_list = Vehicle.objects.filter(number__contains=number).exclude(status_id=1)

    # 从session中获取authority_id
    # user_id = int(request.session.get('user_id', 0))
    authority = int(request.session.get('authority_id', 0))

    # 根据用户权限查询需要该用户审核的车辆
    if authority == 2:
        # 环保局
        # 获取查询车辆的审核状态
        status = int(request.GET.get('status', 2))
        vehicle_list = vehicle_list.filter(vehicle_type_id=1)
    else:
        # 交管局
        status = int(request.GET.get('status', 3))

    if status != 0:
        vehicle_list = vehicle_list.filter(status_id=status)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp, 'number': number, 'status': status, 'authority': authority}

    # 保存页面状态到session
    request.session['number'] = number
    request.session['status'] = status
    request.session['page_num'] = page_num

    return render(request, 'verify.html', context)


# 车辆审核通过
def verify_pass(request):
    vehicle_id = int(request.GET.get('vehicle_id', 0))

    if vehicle_id != 0:
        verify_vehicle(vehicle_id)

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 车辆审核不通过
def verify_refuse(request):
    vehicle_id = int(request.GET.get('vehicle_id', 0))

    if vehicle_id != 0:
        truck = Vehicle.objects.get(id=vehicle_id)
        if truck.status_id == 2:
            truck.hbj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        else:
            truck.jgj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        truck.status_id = 5
        refuse_reason = request.GET.get('refuse_reason', '')
        truck.reason = refuse_reason

        truck.save()

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 导出全部待审核车辆
def export_xls(request):
    authority_id = request.session.get('authority_id', 0)
    if authority_id == 2:
        truck_list = Vehicle.objects.filter(status_id=2)
    elif authority_id == 3:
        truck_list = Vehicle.objects.filter(status_id=3)
    elif authority_id == 99:
        truck_list = Vehicle.objects.filter(status_id__in=[2, 3])
    else:
        truck_list = None

    if truck_list:
        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)
        # 设置表头
        title = ['id', '企业名称', '车牌号', '车辆类型', '发动机号', '车辆型号', '注册日期', '运输路线', '审核结果(p-通过, f-不通过)',
                 '未通过原因']
        # 生成表头
        len_title = len(title)
        for i in range(0, len_title):
            if i == 7:
                ws.col(i).width = 256 * 50
            elif i == 8:
                ws.col(i).width = 256 * 30
            else:
                ws.col(i).width = 256 * 20
            ws.write(0, i, title[i])
        # 写入车辆数据
        i = 1
        len_content = len_title - 2
        for truck in truck_list:
            content = [truck.id, truck.enterprise.enterprise_name, truck.number, truck.vehicle_type.name, truck.engine,
                       truck.vehicle_model, str(truck.register_date), truck.route]

            for j in range(0, len_content):
                ws.write(i, j, content[j])
            i += 1

        # 内存文件操作
        buf = io.BytesIO()
        # 将文件保存在内存中
        wb.save(buf)
        response = HttpResponse(buf.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=vehicle_check.xls'
        response.write(buf.getvalue())
        return response
    else:
        # 构建返回url
        number = request.session.get('number', '')
        status = request.session.get('status', '')
        page_num = request.session.get('page_num', '')
        url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

        return HttpResponseRedirect(url)


# 导入审核后的车辆数据
def import_xls(request):
    # 获取用户的权限等级
    authority_id = request.session.get('authority_id', 0)
    # 获取用户上传的excel文件, 文件不存储, 在内存中对文件进行操作
    excel_file = request.FILES.get('excel_file')

    # 打开excel文件, 直接从内存读取文件内容
    workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
    # 获得sheets列表
    sheets = workbook.sheet_names()
    # 获得第一个sheet对象
    worksheet = workbook.sheet_by_name(sheets[0])
    # 遍历
    for i in range(1, worksheet.nrows):
        # 读取一条车辆信息
        # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error

        # 读取车辆id
        if worksheet.cell(i, 0).ctype != 5 and worksheet.cell_value(i, 0) != '':
            vehicle_id = int(worksheet.cell_value(i, 0))  # 车辆id
        else:
            continue

        # 根据车辆id从数据库查询该车辆
        try:
            truck = Vehicle.objects.get(id=vehicle_id)
        except Exception as e:
            print(e)
            continue

        if truck.status_id != 2 and truck.status_id != 3:
            continue
        elif authority_id == 2 and truck.status_id != 2:
            continue
        elif authority_id == 3 and truck.status_id != 3:
            continue

        # 读取审核状态
        if worksheet.cell(i, 8).ctype != 5 and worksheet.cell_value(i, 8) != '':
            vehicle_status = str(worksheet.cell_value(i, 8))  # 审核状态
        else:
            continue

        # 记录审核时间
        if truck.status_id == 2:
            truck.hbj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        else:
            truck.jgj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # 审核通过
        if 'p' in vehicle_status.lower():
            truck.status_id += 1
        # 审核不通过
        elif 'f' in vehicle_status.lower():
            truck.status_id = 5
            # 读取未通过原因
            if worksheet.cell(i, 9).ctype != 5 and worksheet.cell_value(i, 9) != '':
                truck.reason = worksheet.cell_value(i, 9)  # 未通过原因

            # 存入数据库
            try:
                truck.save()
            except Exception as e:
                print(e)
        else:
            continue

        # 完全通过审核, 生成通行证图片
        if truck.status_id == 4:
            verify_vehicle_pass(truck)

    return HttpResponseRedirect('/verify')


# 清空本单位全部车辆
def clear_all(request):
    user_id = request.GET.get('user_id', 0)

    if user_id != 0:
        Vehicle.objects.filter(enterprise_id=user_id).delete()

    return HttpResponseRedirect('/vehicle')


# 判断该号牌车辆是否已经存在
def is_vehicle_exist(request):
    number = request.GET.get('number', '')

    result = False
    if number:
        result = Vehicle.objects.filter(number=number).exists()

    return JsonResponse({'result': result})


# 导出通过车辆数据给电警平台
def export_to_ep(request):

    authority_id = request.session.get('authority_id', 0)

    if authority_id in (3, 99):
        truck_list = Vehicle.objects.filter(status_id=4)
    else:
        truck_list = None

    if truck_list:

        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)

        # 设置表头
        title = ['ID', 'HPHM', 'HPZL', 'WFDM', 'QSSJ', 'JZSJ']

        # 生成表头
        len_col = len(title)
        for i in range(0, len_col):
            ws.write(0, i, title[i])

        # 写入车辆数据
        i = 1
        for truck in truck_list:

            # 号牌号码
            hphm = truck.number

            # 号牌种类
            if truck.vehicle_type_id == 1:
                hpzl = '01'
            elif truck.vehicle_type_id == 2:
                hpzl = '02'
            else:
                hpzl = '15'

            # id, 根据车辆id, 号牌号码, 号牌种类经过md5加密生成
            truck_id = hashlib.md5(('%d%s%s' % (truck.id, hphm, hpzl)).encode('utf-8')).hexdigest()

            # 违法代码
            wfdm = '13444'

            # 起始时间
            qssj = truck.start_time.strftime('%Y-%m-%d %H:%M:%S')

            # 截止时间
            jzsj = truck.end_time.strftime('%Y-%m-%d %H:%M:%S')

            # 生成excle内容: ['ID', 'HPHM', 'HPZL', 'WFDM', 'QSSJ', 'JZSJ']
            content = [truck_id, hphm, hpzl, wfdm, qssj, jzsj]

            for j in range(0, len_col):
                ws.write(i, j, content[j])
            i += 1

        # 内存文件操作
        buf = io.BytesIO()

        # 将文件保存在内存中
        wb.save(buf)
        response = HttpResponse(buf.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=vehicle_to_ep.xls'
        response.write(buf.getvalue())
        return response
    else:
        # 构建返回url
        number = request.session.get('number', '')
        status = request.session.get('status', '')
        page_num = request.session.get('page_num', '')
        url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

        return HttpResponseRedirect(url)


def download_certification(request):
    file_name = request.GET.get('file_name')
    month = int(request.GET.get('month', 1))

    if month == 1:
        file_path = r'%s/certification/%s' % (settings.FILE_DIR, file_name)
    else:
        file_path = r'%s/certification_backup/%s' % (settings.FILE_DIR, file_name)

    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_name
    return response


def make_certification(request):

    id_start = '201905'
    limit_data = '2019年5月1日 — 2019年5月31日'

    vehicle_list = VehicleMan.objects.all()

    for truck in vehicle_list:
        truck.cert_id = '%s%s%d%d%d%d' % (id_start, truck.number[1:].strip(), random.randint(0, 9),
                                           random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

        truck.file_name = '%s.jpg' % truck.cert_id
        generate_certification(truck.cert_id, limit_data, truck.number, truck.enterprise.enterprise_name, truck.route,
                               truck.file_name)

        # 存入数据库
        try:
            truck.save()
        except Exception as e:
            print(e)

    return HttpResponse('Ok')