"""
系统参数
"""


class SysInfo(object):
    def __init__(self):
        self.recv_data = {}

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):
        # 保存路口id
        self.recv_data = recv_data_dict.get('SignalControlerIDList', {}).get('SignalControlerID', [])
        self.save_data_to_file('../data/signal_list.txt')

        # 保存区域id
        self.recv_data = [recv_data_dict.get('RegionIDList', {}).get('RegionID', [])]
        self.save_data_to_file('../data/region_list.txt')

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



