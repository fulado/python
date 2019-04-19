"""
项目工具
"""
from tj_orta import settings
from PIL import Image, ImageFont, ImageDraw
import qrcode
import time
import datetime
import calendar
import random

from .models import Vehicle

# 生成通行证图片
def generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name):
    # 设置输出文字内容
    title = '外环线载货汽车日间通行证'
    certification_id = '编号：%s' % certification_id
    limit_data = '有效期：%s' % limit_data
    number = '牌照号：%s' % number
    enterprise_name = '所属企业: %s' % enterprise_name
    route = '行驶路线：%s' % route

    instrument_title = '使用说明'
    instrument_line_1 = '1.持此证每日9时至16时可在外环线上按照证上指定路线行驶。'
    instrument_line_2 = '2.未按规定配装密闭装置从事散体物料运输的车辆使用此证无效。'
    instrument_line_3 = '3.装载货物必须符合有关道路交通管理法律法规对车辆装载的规定以及市政管理部门相关道路、桥梁限载的规定。'
    instrument_line_4 = '4.此证由申请人自助打印，不收取任何费用。'
    instrument_line_5 = '5.此证随车携带，放置在车辆前风挡玻璃明显处。'
    instrument_line_6 = '6.自觉遵守道路交通安全法规，服从交通民警的检查和指挥。'

    # 定义图片尺寸, 创建图片对象
    width = 1123
    height = 794
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建Font对象:
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 40)

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 输出文字:
    draw.text((330, 100), title, font=font, fill=(0, 0, 0))

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
    draw.text((70, point_y), route, font=font, fill=(0, 0, 0))
    point_y += step_y

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
    point_y += step_y
    draw.text((70, point_y), instrument_line_6, font=font, fill=(0, 0, 0))

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


if __name__ == '__main__':
    generate_certification('12345', '2018年5月31日', '津A12345', '哇哈哈哈哈哈哈', '牛牛牛', 'test_123.jpg')


# 车辆审核
def verify_vehicle(vehicle_id):

    try:
        truck = Vehicle.objects.get(id=vehicle_id)
    except Exception as e:
        print(e)

    # 判断车辆审核状态
    if truck.status_id == 2:
        truck.hbj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    else:
        truck.jgj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    truck.status_id += 1

    # 审核通过
    if truck.status_id == 4:
        verify_vehicle_pass(truck)


# 车辆审核通过
def verify_vehicle_pass(truck):
    # 生成通行证图片
    # 生成通行证id, 201805+车牌号+三位随机数
    # 获取当前年, 月
    submit_time = truck.submit_time

    year = submit_time.timetuple().tm_year
    month = submit_time.timetuple().tm_mon
    day = 1

    month_verify = time.localtime().tm_mon

    # 如果提交时间不等于审核时间，通行证开始日期为审核通过的后一天
    if month != month_verify:
        day = time.localtime().tm_mday + 1

    # 如果是12月, 则年+1, 月变为1; 否则, 月+1
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

    end_day = calendar.monthrange(year, month)[1]

    # 防止其实日期带截止日期
    if day > end_day:
        day = end_day

    # 保存通行证有效期起止时间
    truck.start_time = datetime.datetime(year, month, day)

    # 通行证截止日期为下个月的1日0点，此数据导出给电警平台使用
    if month == 12:
        end_month = 1
        end_year = year + 1
    else:
        end_month = month + 1
        end_year = year

    truck.end_time = datetime.datetime(end_year, end_month, 1)

    if month < 10:
        id_start = '%d0%d' % (year, month)
    else:
        id_start = '%d%d' % (year, month)

    certification_id = '%s%s%d%d%d' % (id_start, truck.number[1:].strip(), random.randint(0, 9),
                                       random.randint(0, 9), random.randint(0, 9))
    truck.cert_id = certification_id
    # 计算通行证截至日期
    end_day = calendar.monthrange(year, month)[1]
    limit_data = '%d年%d月%d日 — %d年%d月%d日' % (year, month, day, year, month, end_day)
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
