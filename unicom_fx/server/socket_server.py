import xmltodict
import time
from socketserver import BaseRequestHandler
from threading import Thread

from server.xml_handler import XmlHandler
from server.sys_data import HearBeat, LoginData, CrossReportCtrl


# 创建BaseRequestHandler的子类
class MyRequestHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(MyRequestHandler, self).__init__(request, client_address, server)
        self.request_data = None
        self.response_data = None
        self.xml_handler = None
        self.heart_beat_data = None
        self.token = ''
        self.request_object = None
        self.heart_beat_thread = None

    def setup(self):
        print('建立客户端连接')
        print(self.client_address)

        # 初始化参数
        self.request_data = None
        self.response_data = None
        self.xml_handler = None
        self.heart_beat_data = None
        self.token = ''
        self.request_object = None
        self.heart_beat_thread = None

        # 创建一个xml处理器对象
        self.xml_handler = XmlHandler()

    # 重写handle方法，处理收数据
    def handle(self):
        try:
            while True:
                self.request_data = (self.request.recv(100000)).decode('utf-8')
                self.handle_data()

                if self.response_data:
                    self.request.send(self.response_data.encode())
        except Exception as e:
            print(e)

    def finish(self):
        print('连接关闭')
        # 关闭连接后重置系统参数
        self.request_data = None
        self.response_data = None
        self.xml_handler = None
        self.heart_beat_data = None
        self.token = ''
        self.request_object = None
        self.heart_beat_thread = None

        self.request.close()

    # 发送心跳数据线程
    def send_heart_beat(self):
        while True:
            # 如果token为空，跳出循环
            if self.token == '':
                break
            else:
                self.request.send(self.heart_beat_data.encode())
                print('send_heart_beat')

            # 心跳间隔时间
            time.sleep(5)

    # 处理数据
    def handle_data(self):
        try:
            self.xml_handler.xml_parse(self.request_data.strip())
        except Exception as e:
            print(e)
            return

        # 处理数据
        if self.xml_handler.object_type == 'SDO_User':  # 登录
            print('登录')
            self.login_data()
            time.sleep(1)
            self.cross_report_ctrl()
        elif self.xml_handler.object_type == 'SDO_HeartBeat':  # 心跳
            print('心跳')
            self.heart_beat()
        else:
            return

        self.xml_handler.xml_construct(self.request_object.response_data, self.request_object.data_type, self.token)

        self.response_data = self.xml_handler.response_data_xml

    # 处理登录请求
    def login_data(self):
        self.request_object = LoginData(self.xml_handler.request_data_dict)
        self.request_object.set_response_data()

        # 设置token
        self.token = self.request_object.token

    # 心跳
    def heart_beat(self):
        # 生成心跳xml数据
        self.request_object = HearBeat()
        self.request_object.set_response_data()

        # 创建一个线程，用于发送心跳数据
        # self.heart_beat_thread = Thread(target=self.send_heart_beat)
        # self.heart_beat_thread.start()

    # 订阅
    def cross_report_ctrl(self):
        # 创建订阅数据
        # 路口周期
        cross_cycle = CrossReportCtrl('CrossCycle')
        cross_cycle.get_cross_id_list()
        cross_cycle.set_response_data()

        self.xml_handler.xml_construct(cross_cycle.response_data, cross_cycle.data_type, self.token)
        self.request.send(self.xml_handler.response_data_xml.encode())
        print('订阅路口周期')

        # 路口阶段
        cross_stage = CrossReportCtrl('CrossStage')
        cross_stage.get_cross_id_list()
        cross_stage.set_response_data()

        self.xml_handler.xml_construct(cross_stage.response_data, cross_stage.data_type, self.token)
        self.request.send(self.xml_handler.response_data_xml.encode())
        print('订阅路口阶段')





























