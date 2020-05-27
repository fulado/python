"""
魔兽世界自动登录
"""


import win32gui
import win32api
import win32con
import win32clipboard
import time

from PIL import ImageGrab


# 获得窗口句柄
def get_window_handle(win_name):
    hwnd = win32gui.FindWindow(None, win_name)

    return hwnd


# 获取屏幕尺寸
def get_grab_size_4k(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    return left, top, right * 2, bottom * 2


# 获取屏幕尺寸
def get_screen_size(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    return left, top, right, bottom
    # return left + 875, top + 580, right - 875, bottom - 305


# 获得截图尺寸
def get_grab_size(screen_pos, left, top, width, height):
    left = screen_pos[0] + left
    top = screen_pos[1] + top

    return left, top, left + width, top + height


# 获取屏幕截图
def get_image(image_pos):
    im = ImageGrab.grab(image_pos)
    # im.save('D:/test.png')

    return im


# 内容写入剪切板
def set_cb(content):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, content)
    win32clipboard.CloseClipboard()


# 粘贴剪贴板内容
def paste_cb():
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


# 鼠标定位, 并单击
def click_mouse(pos_x, pos_y):
    win32api.SetCursorPos((pos_x, pos_y))

    # 点击鼠标左键
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos_x, pos_y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos_x, pos_y, 0, 0)


# 清空文本框内容，按delete键5秒
def delete_content():
    win32api.keybd_event(46, 0, 0, 0)
    time.sleep(3)
    win32api.keybd_event(46, 0, win32con.KEYEVENTF_KEYUP, 0)


# 确定登录框位置
def get_login_pos(screen_pos):
    pos_username = (screen_pos[0] + 900, screen_pos[1] + 595)
    pos_password = (screen_pos[0] + 900, screen_pos[1] + 690)
    pos_button_1 = (screen_pos[0] + 900, screen_pos[1] + 770)

    pos_button_2 = (screen_pos[0] + 800, screen_pos[1] + 730)
    pos_button_3 = (screen_pos[0] + 900, screen_pos[1] + 990)
    pos_button_quit = (screen_pos[0] + 900, screen_pos[1] + 585)

    return pos_username, pos_password, pos_button_1, pos_button_2, pos_button_3, pos_button_quit


# 获取用户名和密码
def get_user_info(file_name):
    user_info = []
    file = open(file_name, 'r')
    try:
        for line in file.readlines():
            user_info.append(line.strip())
    except Exception as e:
        print(e)
    finally:
        file.close()
        return user_info


# 登录
def login_action(screen_pos, user_info):
    login_pos = get_login_pos(screen_pos)

    # 确认被踢
    click_mouse(login_pos[5][0], login_pos[5][1])
    time.sleep(1)

    # 输入用户名
    click_mouse(login_pos[0][0], login_pos[0][1])
    # delete_content()
    set_cb(user_info[0])
    paste_cb()
    time.sleep(1)

    # 输入密码
    click_mouse(login_pos[1][0], login_pos[1][1])
    # delete_content()
    set_cb(user_info[1])
    paste_cb()
    time.sleep(1)

    # 点击登录按钮
    click_mouse(login_pos[2][0], login_pos[2][1])
    time.sleep(10)

    # 选择第一个账号
    click_mouse(login_pos[3][0], login_pos[3][1])
    time.sleep(5)

    # 进入游戏
    click_mouse(login_pos[4][0], login_pos[4][1])


# 对比截图, 相同返回True, 不同返回False
def compare_img(img_1, img_2):
    pix_1 = img_1.load()
    pix_2 = img_2.load()

    width = min(img_1.width, img_2.width)
    height = min(img_1.height, img_2.height)

    total = width * height

    if total == 0:
        return False

    # 计算有多少个像素的rgb值不同
    diff = 0
    for x in range(0, width):
        for y in range(0, height):
            rgb_1 = pix_1[x, y]
            rgb_2 = pix_2[x, y]

            if compare_rgb(rgb_1, rgb_2):
                pass
            else:
                diff += 1

    # 如果有超过70%的像素不同, 返回False, 否则返回True
    if diff / total >= 0.7:
        return False
    else:
        return True


# 对比2个像素的rgb值
def compare_rgb(rgb_1, rgb_2):
    if abs(rgb_1[0] - rgb_2[0]) < 10 and abs(rgb_1[1] - rgb_2[1]) < 10 and abs(rgb_1[2] - rgb_2[2]) < 10:
        return True
    else:
        return False


# 每两分钟对比一下是否已经返回登录界面
def check_return_to_login(image_base, image_pos):
    image_now = get_image(image_pos)


# 提示xinxi
def show_msg():
    print('请用鼠标点击魔兽窗口, 保持魔兽世界窗口在最前端, 不被其它窗口遮挡, 鼠标不要遮挡魔兽世界logo')
    time.sleep(3)
    print()
    print('5秒后开始自动登录')
    for i in range(0, 5):
        print(5 - i)

    print()
    print('开始自动登录')


# 主函数
def main():
    show_msg()
    win_name = '魔兽世界'
    hwnd = get_window_handle(win_name)
    screen_pos = get_screen_size(hwnd)
    print(screen_pos)

    image_pos = get_grab_size(screen_pos, 30, 58, 303, 128)
    image_base = get_image(image_pos)

    # 读取用户信息
    file_name = r'C:/wow/account.txt'
    user_info = get_user_info(file_name)

    login_action(screen_pos, user_info)

    # 每分钟对比一下是否已经返回登录界面
    while True:
        time.sleep(60)

        image_now = get_image(image_pos)

        if compare_img(image_base, image_now):
            # 相同则已经返回登录界面
            login_action(screen_pos, user_info)
        else:
            # 不同则没有被踢
            pass


if __name__ == '__main__':
    main()


