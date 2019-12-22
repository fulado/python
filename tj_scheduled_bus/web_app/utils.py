"""
工具函数
"""
from tj_scheduled_bus import settings
from django.core.paginator import Paginator
from .models import Statistic, Enterprise, Route
from PIL import Image, ImageFont, ImageDraw

import qrcode
import requests
import json
import time
import random
import calendar


# 分页工具类
class MyPaginator(object):
    def __init__(self):
        self.page_range = []        # 页码范围
        self.show_begin = False     # 显示首页
        self.show_end = False       # 显示尾页
        self.object_list = []       # 当前页数据
        self.current_num = 0        # 当前页码
        self.total_objects = 0      # 共计多少条数据
        self.total_pages = 0        # 共计多少页

    def paginate(self, item_list, item_num, user_num):
        """
        :param item_list: 分页数据列表
        :param item_num: 每页显示几条数据
        :param user_num: 用户给定页码
        :return:
        """
        self.total_objects = len(item_list)

        p = Paginator(item_list, item_num)

        # 共计多少页
        self.total_pages = p.num_pages

        # 防止当用户给出的page_num超出分页范围
        if int(user_num) < 1:
            user_num = 1
        elif int(user_num) > p.num_pages:
            user_num = p.num_pages
        self.current_num = user_num

        # 计算显示的起始页码和结束页码, 默认显示5页
        begin_page = int(user_num) - 2
        end_page = int(user_num) + 2

        if begin_page < 1:
            begin_page = 1
        if end_page > p.num_pages:
            end_page = p.num_pages

        self.page_range = range(begin_page, end_page + 1)

        # 是否显示首尾页标识
        if begin_page > 1:
            self.show_begin = True
        else:
            self.show_begin = False

        if end_page < p.num_pages:
            self.show_end = True
        else:
            self.show_end = False

        # 返回的当页数据
        self.object_list = p.page(user_num)


# 保存文件
def save_file(file_obj, file_name):
    full_name = r'%s/file/%s.png' % (settings.FILE_DIR, file_name)
    f = open(full_name, 'wb')

    for chunk in file_obj.chunks():
        f.write(chunk)

    f.close()


# 保存解冻文件
def save_unlock_file(file_obj, file_name):
    full_name = r'%s/file/%s' % (settings.FILE_DIR, file_name)
    f = open(full_name, 'wb')

    for chunk in file_obj.chunks():
        f.write(chunk)

    f.close()


# 通行证统计+1
def statistic_update(enterprise_id, end_date):
    sta_list = Statistic.objects.filter(sta_enterprise_id=enterprise_id).filter(sta_date=end_date)

    if sta_list:
        sta_info = sta_list[0]
    else:
        sta_info = Statistic()
        sta_info.sta_enterprise_id = enterprise_id
        sta_info.sta_date = end_date

    sta_info.permission_count += 1
    sta_info.save()


# 发送短信验证码
def send_sms(phone_number, sms_code):
    url = 'http://111.160.75.93:20700/llt-rpc/rest/sms'

    msg = '您的验证码是：%s。请不要把验证码泄露给其他人。' % sms_code

    # 请求头
    headers = {'app-name': 'bcz',
               'content-type': 'application/x-www-form-urlencoded',
               'is-test': 'true',
               }

    # 请求体
    data = {
        "mobile": phone_number,
        "msg": msg,
    }

    response_data = requests.post(url, headers=headers, data=data)
    result = (json.loads(response_data.content.decode())).get('result', -1)

    if result == 0:
        return True
    else:
        return False


# 查询车辆信息
def get_vehicle_info(vehicle_number, vehicle_type='01'):
    url = 'http://111.160.75.93:20700/llt-rpc/rest/car'

    # 请求头
    headers = {'app-name': 'bcz',
               'is-test': 'true',
               }

    # 附加参数
    params = {
        "hphm": vehicle_number,
        "hpzl": vehicle_type,
    }

    response_data = requests.get(url, params=params, headers=headers)

    if len(response_data.content):
        return json.loads(response_data.content.decode())
    else:
        return None


# 校验车辆信息
def check_vehicle(vehicle_number, engine_code, vehicle_owner):

    # 信息不全不通过
    if len(vehicle_number) * len(engine_code) * len(vehicle_owner) == 0:
        return False

    # 非津牌车辆直接通过
    elif vehicle_number[0] != '津':
        return True

    vehicle_info = get_vehicle_info(vehicle_number)

    # 查询结果为空不通过
    if not vehicle_info:
        return False

    # 发动机号不一致不通过
    elif engine_code != vehicle_info.get('fdjh', ''):
        return False

    # 所有人不一致不通过
    elif vehicle_owner != vehicle_info.get('syr', ''):
        return False

    else:
        return True


# 校验车辆是否在年检期限内，False-过期，True-有效期内
def check_vehicle_expired(vehicle_number):
    # 信息不全不通过
    if vehicle_number is None:
        return False

    # 非津牌车辆直接通过
    elif vehicle_number[0] != '津':
        return True

    vehicle_info = get_vehicle_info(vehicle_number)

    # 查询结果为空不通过
    if not vehicle_info:
        return False

    # 判断有效期
    expired_date = vehicle_info.get('yxqz', '')

    if expired_date == '':
        return False

    expired_date = time.strptime(expired_date, '%Y-%m-%d %H:%M:%S')

    if expired_date >= time.localtime():
        return True
    else:
        return False


# 申请通行证
def create_permission(permission_info):
    # 有效日期
    current_time = time.localtime()
    year = current_time.tm_year
    month = current_time.tm_mon
    start_day = current_time.tm_mday
    end_day = calendar.monthrange(year, month)[1]

    start_date = '%s-%s-%s' % (year, month, start_day)
    end_date = '%s-%s-%s' % (year, month, end_day)

    permission_info.start_date = start_date
    permission_info.end_date = end_date

    certification_id = '%d%d%s%d%d%d%d' % (year, month,
                                           permission_info.permission_vehicle.vehicle_number[1:].strip(),
                                           random.randint(0, 9),
                                           random.randint(0, 9),
                                           random.randint(0, 9),
                                           random.randint(0, 9),
                                           )

    permission_info.permission_id = certification_id
    permission_info.save()

    limit_data = '%d年%d月%d日 — %d年%d月%d日' % (year, month, start_day, year, month, end_day)

    vehicle_number = permission_info.permission_vehicle.vehicle_number
    user_id = permission_info.permission_user_id
    enterprise_name = (Enterprise.objects.get(user_id=user_id, enterprise_type=41)).enterprise_name

    route_info_list = Route.objects.filter(route_name=permission_info.permission_route).filter(route_user_id=user_id)
    route = ''
    for route_info in route_info_list:
        if route != '':
            route += ' — '

        route += route_info.route_station.station_name

    file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)

    generate_certification(certification_id, limit_data, vehicle_number, enterprise_name, route, file_name)


# 生成通行证图片
def generate_certification(certification_id, limit_data, vehicle_number, enterprise_name, route, file_name):
    # 设置输出文字内容
    title = '班车通行证'
    certification_id = '编号：%s' % certification_id
    limit_data = '有效期：%s' % limit_data
    number = '牌照号：%s' % vehicle_number
    enterprise_name = '所属企业: %s' % enterprise_name
    route = '行驶路线：%s' % route

    route_list = list(route)
    i = 1
    while i * 40 < len(route):
        route_list.insert(i * 40, '\n')
        i += 1

    route_print = ''.join(route_list)

    instrument_title = '使用说明'
    instrument_line_1 = '1.在站点停靠需要做到人等车，不能车等人，要做到即停即离。'
    instrument_line_2 = '2.此证书最新的下载日期为有效证数。'
    instrument_line_3 = '3.此证由申请人自助打印，不收取任何费用。'
    instrument_line_4 = '4.此证随车携带，放置在车辆前风挡玻璃明显处。'
    instrument_line_5 = '5.自觉遵守道路交通安全法规，服从交通民警的检查和指挥。'

    # 定义图片尺寸, 创建图片对象
    width = 1123
    height = 794
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建Font对象:
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 40)

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 输出文字:
    draw.text((460, 100), title, font=font, fill=(0, 0, 0))

    point_y = 180
    step_y = 50
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 25)

    draw.text((70, point_y), certification_id, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), limit_data, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), number, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), enterprise_name, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), route_print, font=font, fill=(0, 0, 0))
    point_y += step_y + 20 * i

    # 输出说明文字
    step_y = 40
    draw.text((500, point_y), instrument_title, font=font, fill=(0, 0, 0))
    point_y += step_y
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 20)
    draw.text((70, point_y), instrument_line_1, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), instrument_line_2, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), instrument_line_3, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), instrument_line_4, font=font, fill=(0, 0, 0))
    point_y += step_y
    draw.text((70, point_y), instrument_line_5, font=font, fill=(0, 0, 0))

    # 生成二维码
    data = '%s | %s | %s' % (number, limit_data, route)
    qr_img = generate_qrcode(data)
    qr_img = qr_img.resize((200, 200), Image.ANTIALIAS)
    image.paste(qr_img, (750, 170))

    # 交管局公章
    gz_img = Image.open(r"%s/img/text9.png" % settings.FILE_DIR)
    image.paste(gz_img, (330, 260), mask=gz_img)

    # 保存图片
    image.save(file_name, 'jpeg')


# 生成二维码图片
def generate_qrcode(data):
    qr = qrcode.QRCode(
        version=1,  # version:值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 控制二维码的错误纠正功能。可取值下列4个常量。
        box_size=10,  # 控制二维码中每个小格子包含的像素数。
        border=2,  # 控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）
    )
    # data = '津A56789 | 有效期至：2018年5月31日 | 行驶路线：南昌桥，中北镇，海泰'
    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image(fill_color="black", back_color="white")


# 测试
def my_test():
    vehicle_number = '津A12345'
    engine_code = 'UJC1120951'
    vehicle_owner = '李锡明'

    result = check_vehicle(vehicle_number, engine_code, vehicle_owner)

    print(result)


if __name__ == '__main__':
    my_test()










