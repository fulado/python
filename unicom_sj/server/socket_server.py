import xmltodict
import time
from socketserver import BaseRequestHandler
from threading import Thread

from server.xml_handler import XmlHandler
from server.sys_data import HearBeat, LoginData, CrossReportCtrl
from server.dynamic_data import CrossCycle, CrossStage
from server.static_data import SysInfo, RegionParam


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
        print('%s : 建立客户端连接' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
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

                # if request_data[:5] == '<?xml':
                #     self.request_data = request_data
                # else:
                #     self.request_data += request_data
                #     continue

                print()
                print('==========================接收数据==========================')
                print(self.request_data)
                print('==========================接收完毕==========================')
                print()

                t_test_1 = Thread(target=self.thread_test_1())
                t_test_1.start()

                t_test_2 = Thread(target=self.thread_test_2())
                t_test_2.start()

                break
                self.handle_data()

                if self.response_data:
                    print()
                    print('==========================发送数据==========================')
                    print(self.response_data)
                    self.request.send(self.response_data.encode())
                    print('==========================发送完毕==========================')
                    print()

        except Exception as e:
            print(e)

    def finish(self):
        print('%s : 连接关闭' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        # 关闭连接后重置系统参数
        self.request_data = None
        self.response_data = None
        self.xml_handler = None
        self.heart_beat_data = None
        self.token = ''
        self.request_object = None
        self.heart_beat_thread = None

        self.request.close()

    # 测试线程1
    def thread_test_1(self):
        for i in range(5):
            print('thread test 1: %d' % i)
            time.sleep(1)

    # 测试线程2
    def thread_test_2(self):
        for i in range(5):
            print('thread test 2: %d' % i)
            time.sleep(1)

    # 发送心跳数据线程
    # def send_heart_beat(self):
    #     while True:
    #         # 如果token为空，跳出循环
    #         if self.token == '':
    #             break
    #         else:
    #             self.request.send(self.heart_beat_data.encode())
    #             print('send_heart_beat')
    #
    #         # 心跳间隔时间
    #         time.sleep(5)

    # 处理数据
    def handle_data(self):
        try:
            self.xml_handler.xml_parse(self.request_data.strip())
        except Exception as e:
            print(e)
            return

        # 处理数据
        if self.xml_handler.object_type == 'SDO_User' and self.token == '':  # 登录, 避免重复登陆
            print('%s : 接收登录请求' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.login_data()
            # time.sleep(5)

            # 登陆成功
            if self.token != '':
                # 新建线程，请求静态数据，并订阅动态数据
                init_data_thread = Thread(target=self.init_data)
                init_data_thread.start()

        elif self.xml_handler.object_type == 'SDO_HeartBeat':  # 心跳
            print('%s : 接收心跳请求' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.heart_beat()

        elif self.xml_handler.object_type == 'CrossCycle':  # 实时周期
            print('%s : 接收实时周期' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.cross_cycle()

            return

        elif self.xml_handler.object_type == 'CrossStage':  # 实时阶段
            print('%s : 接收实时阶段' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.cross_stage()

            return

        elif self.xml_handler.object_type == 'SysInfo':  # 系统信息
            print('%s : 接收系统信息' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.recv_sys_info()

            return

        elif self.xml_handler.object_type == 'RegionParam':  # 区域信息
            print('%s : 接收区域信息' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            self.recv_region_param()

            return

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

        if self.token != '':
            print('%s : 登陆成功' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # 心跳
    def heart_beat(self):
        # 生成心跳xml数据
        self.request_object = HearBeat()
        self.request_object.set_response_data()

        # 创建一个线程，用于发送心跳数据
        # self.heart_beat_thread = Thread(target=self.send_heart_beat)
        # self.heart_beat_thread.start()

    # 订阅路口周期
    def cross_report_ctrl_cycle(self):
        # 路口周期
        cross_cycle = CrossReportCtrl('CrossCycle')
        cross_cycle.get_cross_id_list()
        cross_cycle.set_response_data()

        self.xml_handler.xml_construct(cross_cycle.response_data, cross_cycle.data_type, self.token)
        self.request.send(self.xml_handler.response_data_xml.encode())
        print('%s : 订阅路口周期' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print('==========================发送订阅路口周期==========================')
        print(self.xml_handler.response_data_xml)
        print('==========================发送完毕==========================')

    # 订阅路口阶段
    def cross_report_ctrl_phase(self):
        # 路口阶段
        cross_stage = CrossReportCtrl('CrossStage')
        cross_stage.get_cross_id_list()
        cross_stage.set_response_data()

        self.xml_handler.xml_construct(cross_stage.response_data, cross_stage.data_type, self.token)
        self.request.send(self.xml_handler.response_data_xml.encode())
        print('%s : 订阅路口阶段' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print('==========================发送订阅路口阶段==========================')
        print(self.xml_handler.response_data_xml)
        print('==========================发送完毕==========================')

    # 实时周期
    def cross_cycle(self):
        self.request_object = CrossCycle(self.xml_handler.request_data_dict)
        self.request_object.save_data()

    # 实时阶段
    def cross_stage(self):
        self.request_object = CrossStage(self.xml_handler.request_data_dict)
        self.request_object.save_data()

    # 发送系统参数
    def send_sys_info_(self):
        # 构造请求数据
        sys_info = SysInfo()
        sys_info.set_request_data()

        self.xml_handler.xml_construct(sys_info.request_data, sys_info.data_type, self.token)

        # 发送系统参数请求
        print('==========================发送系统请求数据==========================')
        print(self.xml_handler.response_data_xml)
        print('==========================发送完毕==========================')
        self.request.send(self.xml_handler.response_data_xml.encode())

    # 接收系统信息数据
    def recv_sys_info(self):
        self.request_object = SysInfo()
        self.request_object.parse_response_data(self.xml_handler.request_data_dict)

    # 发送区域参数请求
    def send_region_param(self):
        # 构造请求数据
        region_param = RegionParam()
        region_param.set_request_data()

        self.xml_handler.xml_construct(region_param.request_data, region_param.data_type, self.token)

        # 发送系统参数请求
        print('==========================发送区域参数请求==========================')
        print(self.xml_handler.response_data_xml)
        print('==========================发送完毕==========================')
        self.request.send(self.xml_handler.response_data_xml.encode())

    # 接收系统信息数据
    def recv_region_param(self):
        self.request_object = RegionParam()
        self.request_object.parse_response_data(self.xml_handler.request_data_dict)

    # 请求静态数据，并订阅动态数据
    def init_data(self):
        # 发送系统参数请求
        time.sleep(20)
        self.send_sys_info_()
        print('%s : 发送系统信息请求' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        # 发送区域参数请求
        time.sleep(20)
        self.send_region_param()
        print('%s : 发送区域参数请求' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        # 订阅路口实时数据
        time.sleep(20)
        self.cross_report_ctrl_cycle()

        # 订阅路口阶段数据
        time.sleep(20)
        self.cross_report_ctrl_phase()
















