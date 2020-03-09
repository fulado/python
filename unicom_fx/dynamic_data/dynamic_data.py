"""
信号机实时数据
"""


# 数据基类
class DynamicData(object):
    def __init__(self, recv_data_dict):
        self.recv_data_dict = recv_data_dict
        self.file_name = '../data/error.txt'

    # 获取保存文件路径
    def get_file_name(self, data_type_name):
        cross_id = self.recv_data_dict.get('CrossID', 'error')

        if cross_id != 'error':
            self.file_name = '../data/%s/%s.txt' % (data_type_name, cross_id)
        else:
            pass

    # 保存数据
    def save_data_to_file(self):
        file = open(self.file_name, 'w')

        try:
            for k, v in self.recv_data_dict.items():
                file.write('%s, %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()


# # 路口周期
# class CrossCycle(DynamicData):
#     def get_file_name(self):
#         cross_id = self.recv_data_dict.get('CrossID', 'error')
#
#         self.file_name = '../data/cycle_rt/%s.txt' % cross_id
#
#
# # 路口阶段
# class CrossStage(DynamicData):
#     def get_file_name(self):
#         cross_id = self.recv_data_dict.get('CrossID', 'error')
#
#         self.file_name = '../data/stage_rt/%s.txt' % cross_id































