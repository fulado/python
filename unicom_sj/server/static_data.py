"""
信号静态数据，由双向互通主动发送请求，信号系统返回结果
"""
from utils.xml_tools import generate_ordered_dict


# 数据基类
class StaticData(object):
    def __init__(self):
        self.request_data = {}      # 双向互通发送的其请求数据
        self.response_data = {}     # 信号系统返回的数据
        self.token = ''
        self.data_type = 'REQUEST'
        self.operation_order = '5'
        self.operation_name = 'Get'
        self.operation_list = []

    # 生成请求数据
    def set_request_data(self):
        self.request_data = generate_ordered_dict(self.operation_order, self.operation_name, self.operation_list)

    # 保存数据
    def save_data_to_file(self, file_name):
        file = open(file_name, 'w')

        try:
            # for data in self.response_data:
            #     file.write(data)
            #     file.write(',\n')

            for k, v in self.response_data.items():
                file.write('%s, %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()


# 系统参数
class SysInfo(StaticData):
    def __init__(self):
        super(SysInfo, self).__init__()
        object_list = [('ObjName', 'SysInfo'),
                       ('ID', ''),
                       ('No', ''),
                       ]

        self.operation_list = [('TSCCmd', object_list),
                               ]

    # 解析返回结果数据
    def parse_response_data(self, response_data_dict):
        # 保存路口id
        self.response_data = response_data_dict.get('SignalControlerIDList', {}).get('SignalControlerID', [])
        self.save_data_to_file('../data/signal_list.txt')

        # 保存区域id
        self.response_data = [response_data_dict.get('RegionIDList', {}).get('RegionID', [])]
        self.save_data_to_file('../data/region_list.txt')

    # 保存数据
    def save_data_to_file(self, file_name):
        file = open(file_name, 'w')

        try:
            for data in self.response_data:
                file.write(data)
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()


# 区域参数
class RegionParam(StaticData):
    def __init__(self):
        super(RegionParam, self).__init__()
        object_list = [('ObjName', 'RegionParam'),
                       ('ID', '310120000'),
                       ('No', ''),
                       ]

        self.operation_list = [('TSCCmd', object_list),
                               ]

        # 解析返回结果数据

    def parse_response_data(self, response_data_dict):
        # 保存路口id
        self.response_data = response_data_dict.get('CrossIDList', {}).get('CrossID', [])
        self.save_data_to_file('../data/cross_list.txt')

    # 保存数据
    def save_data_to_file(self, file_name):
        file = open(file_name, 'w')

        try:
            for data in self.response_data:
                file.write(data)
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()


# 信号机参数
class SignalController(StaticData):
    pass


# 信号灯组参数
class LampGroup(StaticData):
    def __init__(self, signal_id):
        super(LampGroup, self).__init__()
        object_list = [('ObjName', 'LampGroup'),
                       ('ID', signal_id),
                       ('No', ''),
                       ]

        self.operation_list = [('TSCCmd', object_list),
                               ]

    # 解析返回结果数据
    def parse_response_data(self, response_data_dict):
        # response_data_dict = response_data_dict.get('SignalControlerID', {})
        self.response_data = response_data_dict

        signal_id = self.response_data.get('SignalControlerID', '')
        file_name = '../data/lamp_group/%s.txt' % signal_id

        self.save_data_to_file(file_name)


# 车道参数
class LaneParam(StaticData):
    def __init__(self, cross_id):
        super(LaneParam, self).__init__()
        object_list = [('ObjName', 'LaneParam'),
                       ('ID', cross_id),
                       ('No', ''),
                       ]

        self.operation_list = [('TSCCmd', object_list),
                               ]

    # 解析返回结果数据
    def parse_response_data(self, response_data_dict):
        # response_data_dict = response_data_dict.get('SignalControlerID', {})
        self.response_data = response_data_dict

        cross_id = self.response_data.get('CrossID', '')
        file_name = '../data/lane_param/%s.txt' % cross_id

        self.save_data_to_file(file_name)


# 相位参数
class PhaseParam(StaticData):
    def __init__(self, cross_id):
        super(PhaseParam, self).__init__()
        object_list = [('ObjName', 'PhaseParam'),
                       ('ID', cross_id),
                       ('No', ''),
                       ]

        self.operation_list = [('TSCCmd', object_list),
                               ]

    # 解析返回结果数据
    def parse_response_data(self, response_data_dict):
        # response_data_dict = response_data_dict.get('SignalControlerID', {})
        self.response_data = response_data_dict

        cross_id = self.response_data.get('CrossID', '')
        file_name = '../data/phase_param/%s.txt' % cross_id

        self.save_data_to_file(file_name)








