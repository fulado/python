"""
信号机实时数据
"""


# 数据基类
class DynamicData(object):
    def __init__(self, data_dict={}):
        self.request_data = data_dict  # 双向互通发送的其请求数据
        self.response_data = {}  # 信号系统返回的数据
        self.token = ''
        self.data_type = 'REQUEST'
        self.operation_order = '5'
        self.operation_name = 'Get'
        self.operation_list = []
        self.file_name = '../data/error.txt'

    #  解析实时数据
    # def parse_data(self, data_dict):
    #     self.request_data = data_dict

    # 保存数据
    def save_data_to_file(self):
        file = open(self.file_name, 'w')

        try:
            for k, v in self.request_data.items():
                file.write('%s, %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()


# 路口周期
class CrossCycle(DynamicData):
    def save_data(self):
        signal_id = self.request_data.get('CrossID', 'error')
        self.file_name = '../data/cycle_rt/%s.txt' % signal_id
        self.save_data_to_file()


# 路口阶段
class CrossStage(DynamicData):
    def save_data(self):
        signal_id = self.request_data.get('CrossID', 'error')
        self.file_name = '../data/phase_rt/%s.txt' % signal_id
        self.save_data_to_file()





























