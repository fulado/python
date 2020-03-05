"""
灯组参数
"""


class LaneParam(object):
    def __init__(self):
        self.recv_data = {}

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):
        self.recv_data = recv_data_dict
        self.save_data_to_file('../data/lamp_group/%s.txt' % recv_data_dict.get('SignalControlerID'))

    # 保存数据
    def save_data_to_file(self, file_name):
        file = open(file_name, 'w')

        try:
            for k, v in self.recv_data.items():
                file.write('%s, %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()



