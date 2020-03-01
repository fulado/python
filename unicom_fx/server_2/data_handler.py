"""
数据处理类
"""
import xmltodict

from .sdo_user import SdoUser
from .sdo_heart_beat import SdoHeartBeat
from .sys_info import SysInfo
from .region_param import RegionParam
from .sys_info_subscribe import SysInfoSubscribe
from .region_param_subscribe import RegionParamSubscribe
from .cross_report_ctrl import CrossReportCtrl
from .dynamic_data import DynamicData


class DataHandler(object):
    def __init__(self, send_data_queue):
        self.send_data_queue = send_data_queue
        self.recv_data_dict = {}
        self.seq = ''
        self.object_type = ''
        self.token = ''

    # 解析xml数据
    def xml_parse(self, recv_data_xml):
        data = xmltodict.parse(recv_data_xml.strip())
        data = data.get('Message', {})

        self.seq = data.get('Seq')
        data = data.get('Body', {}).get('Operation', {})

        self.object_type = tuple(data.keys())[-1]
        self.recv_data_dict = data.get(self.object_type, {})

    # 根据接收数据的类型，处理数据
    def data_handle(self):
        # 登录
        # print(self.object_type)
        if self.object_type == 'SDO_User':
            self.sdo_user_handle()

            if self.token != '':
                # 获取系统信息
                self.sys_info_subscribe_handle()

                # 测试
                # self.cross_report_ctrl_handle()

        # 心跳
        elif self.object_type == 'SDO_HeartBeat':
            self.sdo_heart_beat_handle()

        # 静态数据——系统信息
        elif self.object_type == 'SysInfo':
            self.sys_info_handle()

            # 获取区域信息
            self.region_param_subscribe_handle()

        # 静态数据——区域信息
        elif self.object_type == 'RegionParam':
            self.region_param_handle()

            # 订阅动态数据
            self.cross_report_ctrl_handle()

        # 动态数据——实时周期
        elif self.object_type == 'CrossCycle':
            self.cross_cycle_handle()

        # 动态数据——实时阶段
        elif self.object_type == 'CrossStage':
            self.cross_stage_handle()

        else:
            self.handle_test()

    # 测试
    def handle_test(self):
        print(self.recv_data_dict)
        send_data = 'got it'.encode()
        self.send_data_queue.put(send_data)

    # 登录
    def sdo_user_handle(self):
        sdo_user = SdoUser(self.seq, self.recv_data_dict)
        sdo_user.get_user_info()
        sdo_user.create_send_data()
        sdo_user.put_send_data_into_queue(self.send_data_queue)

        self.token = sdo_user.get_token()
        # print('sdo_user_handle')

    # 心跳
    def sdo_heart_beat_handle(self):
        sdo_heart_beat = SdoHeartBeat(self.seq, self.token)
        sdo_heart_beat.create_send_data()
        sdo_heart_beat.put_send_data_into_queue(self.send_data_queue)

    # 系统信息
    def sys_info_handle(self):
        sys_info = SysInfo()
        sys_info.parse_recv_data(self.recv_data_dict)

    # 区域信息
    def region_param_handle(self):
        region_param = RegionParam()
        region_param.parse_recv_data(self.recv_data_dict)

    # 获取系统信息
    def sys_info_subscribe_handle(self):
        sys_info_subscribe = SysInfoSubscribe(self.token)
        sys_info_subscribe.create_send_data()
        sys_info_subscribe.put_send_data_into_queue(self.send_data_queue)

    # 获取区域信息
    def region_param_subscribe_handle(self):
        region_param_subscribe = RegionParamSubscribe(self.token)
        region_param_subscribe.create_send_data()
        region_param_subscribe.put_send_data_into_queue(self.send_data_queue)

    # 订阅实时数据
    def cross_report_ctrl_handle(self):
        cross_report_ctrl = CrossReportCtrl(self.token)
        cross_report_ctrl.get_cross_id_list()

        # 订阅路口周期
        cross_report_ctrl.create_send_data('CrossCycle')
        cross_report_ctrl.put_send_data_into_queue(self.send_data_queue)

        # 订阅路口阶段
        cross_report_ctrl.create_send_data('CrossStage')
        cross_report_ctrl.put_send_data_into_queue(self.send_data_queue)

    # 路口实时周期
    def cross_cycle_handle(self):
        cross_cycle = DynamicData(self.recv_data_dict)
        cross_cycle.get_file_name('cycle_rt')
        cross_cycle.save_data_to_file()

    # 路口实时阶段
    def cross_stage_handle(self):
        cross_cycle = DynamicData(self.recv_data_dict)
        cross_cycle.get_file_name('stage_rt')
        cross_cycle.save_data_to_file()































