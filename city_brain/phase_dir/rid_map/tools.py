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
    return light_content[-2:]


if __name__ == '__main__':
    a = '盒-1 进-2,出-4,直行'

    f_id = find_froad_id(a)
    t_id = find_troad_id(a)
    turn = find_turn(a)

    print(f_id, t_id, turn)






















