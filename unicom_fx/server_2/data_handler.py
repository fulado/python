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


class DataHandler(object):
    def __init__(self, send_data_queue, queue_put_datahub):
        self.send_data_queue = send_data_queue
        self.queue_put_datahub = queue_put_datahub
        self.recv_data_dict = {}
        self.seq = ''
        self.data_type = ''
        self.object_type = ''
        self.token = ''
        self.data_subscribe = False
        self.signal_id_list = []
        self.cross_id_list = []

    # 解析xml数据
    def xml_parse(self, recv_data_xml):
        data = xmltodict.parse(recv_data_xml.strip())
        data = data.get('Message', {})

        self.token = data.get('Token')
        self.data_type = data.get('Type')
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

        # 心跳
        elif self.object_type == 'SDO_HeartBeat':
            self.sdo_heart_beat_handle()

            # 正常接收心跳数据后发送静态数据请求和动态数据订阅
            if not self.data_subscribe:
                t_data_subscribe_handle = Thread(target=self.data_subscribe_handle)
                t_data_subscribe_handle.start()

                self.data_subscribe = True

        # 静态数据
        elif self.data_type == 'RESPONSE' and self.object_type in \
                ('SysInfo', 'RegionParam', 'LampGroup', 'LaneParam', 'StageParam', 'PlanParam', 'SignalControler'):
            static_data = StaticData(self.object_type)
            static_data.parse_recv_data(self.recv_data_dict)
            static_data.convert_data_for_datahub()

            # 发布到datahub写入队列
            self.queue_put_datahub.put(static_data.datahub_put_data)

            # 保存到本地文件
            static_data.save_data_to_file()

        # 实时数据
        elif self.data_type == 'PUSH' and self.object_type in ('CrossCycle', 'CrossStage') \
                and not isinstance(self.recv_data_dict, list):
            dynamic_data = DynamicData(self.object_type)
            dynamic_data.parse_recv_data(self.recv_data_dict)
            dynamic_data.convert_data_for_datahub()

            # 发布到datahub写入队列
            self.queue_put_datahub.put(dynamic_data.datahub_put_data)

            # 保存到文件
            # dynamic_data.save_data_to_file()

        else:
            pass

    # 测试
    def handle_test(self):
        # print(self.recv_data_dict)
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
        # self.send_data_subscribe(['', ], 'SysInfo')

        # 请求区域信息
        # self.send_data_subscribe(['310120000', ], 'RegionParam')

        # 获取信号id和路口id
        self.get_signal_id_list()
        self.get_cross_id_list()

        # 请求信号机信息
        # self.send_data_subscribe(self.signal_id_list, 'SignalControler')

        # 请求灯组信息
        # self.send_data_subscribe(self.signal_id_list, 'LampGroup')

        # 请求车道信息
        self.send_data_subscribe(self.cross_id_list, 'LaneParam')

        # 请求阶段信息
        # self.send_data_subscribe(self.cross_id_list, 'StageParam')

        # 请求配时方案信息
        # self.send_data_subscribe(self.cross_id_list, 'PlanParam')

        # 订阅实时数据
        self.get_cross_id_list()
        self.cross_report_ctrl_handle()

    # 发送数据查询, 订阅请求
    def send_data_subscribe(self, object_id_list, obj_name):
        for object_id in object_id_list:
            time.sleep(0.1)

            static_data_subscribe = StaticDataSubscribe(self.token, object_id, obj_name)
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






















