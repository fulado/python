"""
相位参数
"""


class StageParam(object):
    def __init__(self):
        self.recv_data = {}

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):
        self.recv_data = recv_data_dict
        self.save_data_to_file('../data/stage_param/%s.txt' % recv_data_dict.get('CrossID'))

    # 保存数据
    def save_data_to_file(self, file_name):
        file = open(file_name, 'w')

        try:
            for k, v in self.recv_data.items():
                if k == 'PhaseNoList':
                    v = self.recv_data.get('PhaseNoList').get('PhaseNo')
                else:
                    pass

                file.write('%s: %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()



