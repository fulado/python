"""
项目工具
"""
from tj_orta import settings
from PIL import Image, ImageFont, ImageDraw
import qrcode


# 生成通行证图片
def generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name):
    # 设置输出文字内容
    title = '外环线载货汽车日间通行证'
    certification_id = '编号：%s' % certification_id
    limit_data = '有效期至：%s' % limit_data
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

