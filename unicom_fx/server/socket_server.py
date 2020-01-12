import xmltodict
import time
from socketserver import BaseRequestHandler
from threading import Thread

from server.xml_handler import XmlHandler
from server.sys_data import HearBeat, LoginData


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

        # 登录
        if self.xml_handler.object_type == 'SDO_User':
            self.login_handle()
        else:
            return

        self.xml_handler.xml_construct(self.request_object.response_date, self.request_object.data_type, self.token)

        self.response_data = self.xml_handler.response_data_xml

    # 处理登录请求
    def login_handle(self):
        self.request_object = LoginData(self.xml_handler.request_data_dict)
        self.request_object.set_response_data()

        # 设置token
        self.token = self.request_object.token

        # token不为空说明登录成功
        if self.token != '':
            # 生成心跳xml数据
            heart_beat = HearBeat()
            heart_beat.set_response_data()
            self.xml_handler.xml_construct(heart_beat.response_data, heart_beat.data_type, self.token)
            self.heart_beat_data = self.xml_handler.response_data_xml

            # 创建一个线程，用于发送心跳数据
            self.heart_beat_thread = Thread(target=self.send_heart_beat)
            self.heart_beat_thread.start()



