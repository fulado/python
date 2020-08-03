import os
import base64
import xlwt


# 读取图片文件, 并做base64编码
def read_file(file_path):
    file = open(file_path, 'rb')

    return base64.b64encode(file.read()).decode()


# 写入数据到excel文件
def export_to_excel(data_list):
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)

    # 设置表头
    title = ['inter_id', 'phase_name', 'phase_state', 'file_content']

    # 生成表头
    len_col = len(title)
    for i in range(0, len_col):
        ws.write(0, i, title[i])

    # 写入车辆数据
    i = 1
    for data in data_list:
        ws.write(i, 0, data['inter_id'])
        ws.write(i, 1, data['phase_name'])
        ws.write(i, 2, data['phase_state'])
        ws.write(i, 3, data['file_content'])
        i += 1

    # 将文件保存在内存中
    wb.save(r'D:\phase_pic.xls')


if __name__ == '__main__':

    path = 'D:/work/2018_上海城市大脑数据接入/03_baoshan/相位图/宝山相位图'
    # path = 'D:/work/2018_上海城市大脑数据接入/02_songjiang/相位图/松江路口相位'

    dir_list = os.listdir(path)

    # print(dir_list)
    pic_list = []

    for dir_name in dir_list:
        dir_path = path + '/' + dir_name
        file_list = os.listdir(dir_path)

        for file_name in file_list:
            file_path = dir_path + '/' + file_name

            file_content = read_file(file_path)

            inter_id = file_name[0: 4]
            phase_name = file_name[-6]
            phase_state = file_name[-5]

            pic_dic = {
                'inter_id': inter_id,   # 宝山
                # 'inter_id': dir_name,   # 松江
                'phase_name': phase_name,
                'phase_state': phase_state,
                'file_content': file_content
            }

            pic_list.append(pic_dic)

    # print(pic_list)
    export_to_excel(pic_list)






