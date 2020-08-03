# 工具


# 在灯组内容字符串中找到进口道id
def find_froad_id(light_content):
    start_pos = light_content.find('进') + 2
    end_pos = light_content.find(',')

    return light_content[start_pos: end_pos]


# 在灯组内容字符串中找到出口道id
def find_troad_id(light_content):
    start_pos = light_content.find('出') + 2
    end_pos = light_content.rfind(',')

    return light_content[start_pos: end_pos]


# 在灯组内容字符串中找到转向描述
def find_turn(light_content):
    if find_froad_id(light_content) == find_troad_id(light_content):
        return '掉头'
    else:
        return light_content[-2:]


# 根据ft_dir确定入口方向
def get_dir_name(ft_dir_4_no):
    if ft_dir_4_no == 1:
        return '北'
    elif ft_dir_4_no == 2:
        return '东'
    elif ft_dir_4_no == 3:
        return '南'
    elif ft_dir_4_no == 4:
        return '西'
    else:
        return '未知'


# 计算转向代码
def get_turn_dir_no(turn):
    if turn == '左转':
        return '1'
    elif turn == '直行':
        return '2'
    elif turn == '右转':
        return '3'
    elif turn == '掉头':
        return '4'
    elif turn == '行人':
        return '5'
    else:
        return '0'


# 计算转向描述
def get_turn_name(turn_dir_no):
    if turn_dir_no == '1':
        return '左转'
    elif turn_dir_no == '2':
        return '直行'
    elif turn_dir_no == '3':
        return '右转'
    elif turn_dir_no == '4':
        return '掉头'
    elif turn_dir_no == '0':
        return '行人'
    else:
        return '未知'


if __name__ == '__main__':
    a = '盒-1 进-2,出-4,直行'

    f_id = find_froad_id(a)
    t_id = find_troad_id(a)
    turn = find_turn(a)

    print(f_id, t_id, turn)






















