"""
数据处理类
"""
import xmltodict


class DataHandler(object):
    def __init__(self, recv_data, send_data_queue):
        self.send_data_queue = send_data_queue
        self.recv_data_xml = recv_data
        self.recv_data_dict = None
        self.seq = None
        self.object_type = None

    # 解析xml数据
    def xml_parse(self):
        data = xmltodict.parse(self.recv_data_xml.strip())
        data = data.get('Message', {})

        self.seq = data.get('Seq')
        data = data.get('Body', {}).get('Operation', {})

        self.object_type = tuple(data.keys())[-1]
        self.recv_data_dict = data.get(self.object_type, {})

    # 根据接收数据的类型，处理数据
    def data_handle(self):
        # 登录
        if self.object_type == 'SDO_User':
            pass

        # 心跳
        elif self.object_type == 'SDO_HeartBeat':
            pass

        # 静态数据——系统信息
        elif self.object_type == 'SysInfo':
            pass

        # 静态数据——区域信息
        elif self.object_type == 'RegionParam':
            pass

        # 动态数据——实时周期
        elif self.object_type == 'CrossCycle':
            pass

        # 动态数据——实时阶段
        elif self.object_type == 'CrossStage':
            pass

        else:
            pass

    # 登录
    def login_handle(self):























