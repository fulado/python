"""
数据处理类
"""
import xmltodict
import time

from threading import Thread
from sys_data.sdo_user import SdoUser
from sys_data.sdo_heart_beat import SdoHeartBeat

from dynamic_data.cross_report_ctrl import CrossReportCtrl
from dynamic_data.dynamic_data import DynamicData
from static_data.static_data import StaticData
from static_data.static_data_subscribe import StaticDataSubscribe

from .datahub_handler import DatahubHandler


class DataHandler(object):
    def __init__(self, send_data_queue):
        self.send_data_queue = send_data_queue
        self.recv_data_dict = {}
        self.seq = ''
        self.object_type = ''
        self.token = ''
        self.data_subscribe = False
        self.signal_id_list = []
        self.cross_id_list = []
        self.dh_handler = DatahubHandler()

    # 解析xml数据
    def xml_parse(self, recv_data_xml):
        data = xmltodict.parse(recv_data_xml.strip())
        data = data.get('Message', {})

        self.token = data.get('Token')
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

            # if self.token != '':
            #     # 获取系统信息
            #
            #     t_sys_info_subscribe_handle = Thread(target=self.sys_info_subscribe_handle)
            #     t_sys_info_subscribe_handle.start()

            # 测试
            # self.cross_report_ctrl_handle()

        # 心跳
        elif self.object_type == 'SDO_HeartBeat':
            self.sdo_heart_beat_handle()

            # 正常接收心跳数据后发送静态数据请求和动态数据订阅
            if not self.data_subscribe:
                t_data_subscribe_handle = Thread(target=self.data_subscribe_handle)
                t_data_subscribe_handle.start()

                self.data_subscribe = True

        # 静态数据
        elif self.object_type in ('SysInfo', 'RegionParam', 'LampParam', 'LaneParam', 'StageParam', 'PlanParam'):
            static_data = StaticData(self.object_type)

            static_data.parse_recv_data(self.recv_data_dict)
            static_data.save_data_to_file()

        # 实时数据
        elif self.object_type in ('CrossCycle', 'CrossStage'):
            dynamic_data = DynamicData()

            dynamic_data.parse_recv_data(self.recv_data_dict)
            dynamic_data.save_data_to_file()

        else:
            pass
            # self.handle_test()

    # 测试
    def handle_test(self):
        print(self.recv_data_dict)
        send_data = 'got it'.encode()
        self.send_data_queue.put(send_data)

    # 登录
    def sdo_user_handle(self):

        sdo_user = SdoUser(self.seq, self.token, self.recv_data_dict)
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

    # 请求静态数据，并订阅实时数据
    def data_subscribe_handle(self):

        # 请求系统信息
        self.send_data_subscribe('', 'SysInfo')

        # 请求区域信息
        self.send_data_subscribe('310120000', 'RegionParam')

        # # 请求灯组信息
        # self.get_signal_id_list()
        #
        # for signal_id in self.signal_id_list:
        #     self.send_data_subscribe(signal_id, 'LampGroup')

        # 请求车道信息
        # self.get_cross_id_list()
        #
        # for cross_id in self.cross_id_list:
        #     self.send_data_subscribe(cross_id, 'LaneParam')
        #
        # # 实时数据订阅
        # self.cross_report_ctrl_handle()

    # 发送数据查询, 订阅请求
    def send_data_subscribe(self, cross_id, obj_name):
        time.sleep(1)

        static_data_subscribe = StaticDataSubscribe(self.token, cross_id, obj_name)
        static_data_subscribe.create_send_data()
        static_data_subscribe.put_send_data_into_queue(self.send_data_queue)

    # 获取信号灯id列表
    def get_signal_id_list(self):
        file = open('../data/signal_list.txt', 'r')

        try:
            for line in file.readlines():
                self.signal_id_list.append(line.strip())

        except Exception as e:
            print(e)
        finally:
            file.close()

    # 获取路口id列表
    def get_cross_id_list(self):
        file = open('../data/cross_list.txt', 'r')

        try:
            for line in file.readlines():
                self.cross_id_list.append(line.strip())

        except Exception as e:
            print(e)
        finally:
            file.close()

    # 订阅实时数据
    def cross_report_ctrl_handle(self):
        cross_report_ctrl = CrossReportCtrl(self.token)
        cross_report_ctrl.set_cross_id_list(self.cross_id_list)

        # 订阅路口周期
        cross_report_ctrl.create_send_data('CrossCycle')
        cross_report_ctrl.put_send_data_into_queue(self.send_data_queue)

        # 订阅路口阶段
        time.sleep(1)
        cross_report_ctrl.create_send_data('CrossStage')
        cross_report_ctrl.put_send_data_into_queue(self.send_data_queue)






















