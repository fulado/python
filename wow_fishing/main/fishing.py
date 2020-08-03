import win32gui
import win32api
import win32con
import time

from PIL import ImageGrab


# 获得窗口句柄
def get_window_handle(win_name):
    hwnd = win32gui.FindWindow(None, win_name)

    # 获得DC
    # hdc = win32gui.GetWindowDC(hwnd)

    return hwnd


# 获取屏幕截图位置
def get_grab_size_4k(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print(left, top, right, bottom)
    right *= 2
    bottom *= 2

    # print(left, top, right, bottom)

    left += 1500
    right -= 1500
    top += 200
    bottom -= 600

    # print(left, top, right, bottom)

    return left, top, right, bottom


# 获取屏幕截图位置
def get_grab_size(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print(left, top, right, bottom)
    left += 750
    right -= 750
    top += 100
    bottom -= 300
    # print(left, top, right, bottom)
    return left, top, right, bottom


# 获取屏幕截图
def get_image(image_pos):
    im = ImageGrab.grab(image_pos)
    im.save('D:/test.png')

    return im


# 计算当前rgb与目标rgb的绝对值差值，如果插值小于20，返回True，否者返回False
def compare_rgb(rgb, target_rgb):
    if abs(rgb[0] - target_rgb[0]) < 20 and abs(rgb[1] - target_rgb[1]) < 20 and abs(rgb[2] - target_rgb[2]) < 20:
    # if abs(rgb[0] - target_rgb[0]) + abs(rgb[1] - target_rgb[1]) + abs(rgb[2] - target_rgb[2]) < 30:
        return True
    else:
        return False


# 根据屏幕截图和给出rgb值，找到坐标点
def get_pos(im, image_pos, target_rgb):
    pix = im.load()

    x = 0
    find_it = False
    pos_x = 0
    pos_y = 0

    while x < im.width:
        y = 0
        while y < im.height:
            rgb = pix[x, y]

            if compare_rgb(rgb, target_rgb):
                # print(rgb)
                pos_x = image_pos[0] + x
                pos_y = image_pos[1] + y

                find_it = True
                break
            else:
                y += 3

        if find_it:
            break
        else:
            x += 3

    # pos_x = int(pos_x / 2)
    # pos_y = int(pos_y / 2)
    pos_x = int(pos_x)
    pos_y = int(pos_y)

    return pos_x, pos_y


# 首次甩出鱼漂
def throw_float():
    print('====== 请用鼠标点击魔兽窗口, 保持魔兽世界窗口在最前端, 不被其它窗口遮挡并为活跃窗口, 然后将鼠标移至屏幕边缘 ======')
    time.sleep(5)

    print()
    print('====== 5秒后开始识别鱼漂 ======')
    for i in range(5):
        print('====== %d ======' % (5 - i))
        time.sleep(1)

    win32api.keybd_event(81, 0, 0, 0)
    win32api.keybd_event(81, 0, win32con.KEYEVENTF_KEYUP, 0)

    print()
    print('====== 甩出鱼漂 ======')
    time.sleep(5)
    print('====== 开始识别鱼漂 ======')


# 找到鱼漂的rgb值
def get_rgb_float(im):
    # 甩出鱼漂, 取截图rgb的平均值, 然后计算每个点与平均值的差值, 找出插值最大的点, 作为鱼漂的坐标

    pix = im.load()

    r = 0
    g = 0
    b = 0

    num = 0
    for x in range(0, im.width, 2):
        for y in range(0, im.height, 2):
            rgb = pix[x, y]
            r += rgb[0]
            g += rgb[1]
            b += rgb[2]

            num += 1

    avg_rgb = (int(r / num), int(g / num), int(b / num))

    # print(avg_rgb, num)

    max_diff = 0
    pos_x = 0
    pos_y = 0

    for x in range(0, im.width, 2):
        for y in range(0, im.height, 2):
            rgb = pix[x, y]

            diff = abs(rgb[0] - avg_rgb[0]) + abs(rgb[0] - avg_rgb[0]) + abs(rgb[0] - avg_rgb[0])
            if diff > max_diff:
                max_diff = diff
                pos_x = x
                pos_y = y
            else:
                pass

    # print(pix[pos_x, pos_y])
    print('====== 识别鱼漂完成 ======')
    return pix[pos_x, pos_y]


# 甩杆
def start_fishing(image_pos, target_rgb):
    # 1. 按键盘q键 甩杆
    # 2. 判断pos_x, pos_y值, 不为零甩杆完成，并返回鱼漂位置坐标
    pos_x = 0
    pos_y = 0

    while pos_x == 0 and pos_y == 0:
        win32api.keybd_event(81, 0, 0, 0)
        win32api.keybd_event(81, 0, win32con.KEYEVENTF_KEYUP, 0)
        print()
        print('====== 甩杆 ======')

        # 等待3秒，鱼漂稳定
        time.sleep(3.5)

        # 观察甩杆是否成功，获取屏幕截图
        image = get_image(image_pos)
        pos_x, pos_y = get_pos(image, image_pos, target_rgb)

    return pos_x, pos_y


# 定位鱼漂
def locate_fishing(pos_x, pos_y):
    win32api.SetCursorPos((pos_x, pos_y))
    print('====== 定位 ======')

    time.sleep(1)


# 收杆
def finish_fishing(image_pos, target_rgb):
    # 1. 判断pos_x, pos_y值，如果不为零，说明鱼已经咬钩
    # 2. 点击鼠标右键收杆
    pos_x = 0
    pos_y = 0
    waiting_times = 0

    while pos_x == 0 and pos_y == 0 and waiting_times < 60:
        # 观察甩杆是否成功，获取屏幕截图
        image = get_image(image_pos)
        pos_x, pos_y = get_pos(image, image_pos, target_rgb)

        time.sleep(0.2)
        waiting_times += 1

    # 人脑反应没那么块，这里再延迟0.5秒
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos_x, pos_y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos_x, pos_y, 0, 0)
    print('====== 收杆 ======')

    time.sleep(2)


# 上鱼饵
def add_fish_food():
    # 鼠标移动到鱼饵
    pos_x = 1840
    pos_y = 300
    win32api.SetCursorPos((pos_x, pos_y))
    time.sleep(0.5)

    # 点击右键
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos_x, pos_y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos_x, pos_y, 0, 0)
    time.sleep(0.5)

    # 鼠标移动到鱼竿
    pos_y += 50
    win32api.SetCursorPos((pos_x, pos_y))
    time.sleep(0.5)

    # 点击左键
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos_x, pos_y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos_x, pos_y, 0, 0)
    time.sleep(7)


# 准备钓鱼
def prepare_fishing():
    print()
    for i in range(5):
        print('====== %d秒后开始钓鱼 ======' % (5 - i))
        time.sleep(1)


# 主函数
def main():
    win_name = '魔兽世界'
    hwnd = get_window_handle(win_name)

    image_pos = get_grab_size(hwnd)
    throw_float()
    im_float = get_image(image_pos)

    target_rgb_float = get_rgb_float(im_float)
    target_rgb_got = (140, 190, 140)  # 鱼上钩后的rgb值

    prepare_fishing()

    # 上鱼饵
    # add_fish_food()

    # 开始钓鱼
    # start_time = int(time.time())
    while True:
        pos_x, pos_y = start_fishing(image_pos, target_rgb_float)
        locate_fishing(pos_x, pos_y)
        finish_fishing(image_pos, target_rgb_got)

        # 当前时间
        # now_time = int(time.time())

        # # 如果时间间隔大于10分钟，重新上鱼饵
        # if now_time - start_time > 620:
        #     add_fish_food()
        #     start_time = int(time.time())
        # else:
        #     pass


if __name__ == '__main__':
    main()






















