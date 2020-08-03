"""
区域参数
"""


class RegionParam(object):
    def __init__(self):
        self.recv_data = {}

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):
        self.recv_data = recv_data_dict.get('CrossIDList', {}).get('CrossID', [])
        self.save_data_to_file('../data/cross_list.txt')

    # 保存数据
    def save_data_to_file(self, file_name):
        file = open(file_name, 'w')

        try:
            for data in self.recv_data:
                file.write(data)
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()



