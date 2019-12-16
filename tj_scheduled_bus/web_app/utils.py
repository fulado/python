"""
工具函数
"""
from tj_scheduled_bus import settings
from django.core.paginator import Paginator
from .models import Statistic

import requests
import json


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


# 测试
def my_test():
    vehicle_number = '津A12345'
    engine_code = 'UJC1120951'
    vehicle_owner = '李锡明'

    result = check_vehicle(vehicle_number, engine_code, vehicle_owner)

    print(result)


if __name__ == '__main__':
    my_test()










