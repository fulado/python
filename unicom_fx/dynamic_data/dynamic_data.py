"""
信号机实时数据
"""


# 数据基类
class DynamicData(object):
    def __init__(self, obj_name):
        self.recv_data = {}
        self.obj_name = obj_name
        self.file_name = '../data/error.txt'

    # 获取保存文件路径
    def parse_recv_data(self, recv_data_dict):
        cross_id = recv_data_dict.get('CrossID', 'error')

        if cross_id != 'error':

            if self.obj_name == 'CrossCycle':
                self.file_name = '../data/%s/%s.txt' % ('cycle_rt', cross_id)
            elif self.obj_name == 'CrossStage':
                self.file_name = '../data/%s/%s.txt' % ('stage_rt', cross_id)
            else:
                pass

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































