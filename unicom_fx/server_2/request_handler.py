import time

from socketserver import BaseRequestHandler
from multiprocessing import Queue
from threading import Thread, local
from .utils import create_logger, print_log, xml_check
from .data_handler import DataHandler


# BaseRequestHandler子类
class MyRequestHandler(BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super(MyRequestHandler, self).__init__(request, client_address, server)
        self.queue_recv_data = None  # 接收数据队列
        self.queue_send_data = None  # 发送数据队列
        self.connection_status = False
        self.t_handle_data_status = False
        self.t_send_data_status = False
        self.logger_recv = None
        self.logger_send = None

    def setup(self):
        print('%s : 连接建立, %s:%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                                    self.client_address[0], self.client_address[1]))
        self.connection_status = True
        self.queue_recv_data = Queue(50)  # 接收数据队列
        self.queue_send_data = Queue(50)  # 发送数据队列
        self.logger_recv = create_logger('recv')
        self.logger_send = create_logger('send')

    def handle(self):
        # 处理数据线程
        t_handle_data = Thread(target=self.thread_handle_data)
        t_handle_data.start()

        # 创建并启动发送数据线程
        t_send_data = Thread(target=self.thread_send_data)
        t_send_data.start()

        # 创建并启动接收数据线程
        # t_recv_data = Thread(target=self.thread_recv_data)
        # t_recv_data.start()
        # t_recv_data.join()

        self.thread_recv_data()

    def finish(self):
        print('%s : 连接关闭' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        # global connection_status
        self.connection_status = False

    # 接收数据线程
    def thread_recv_data(self):
        recv_data = ''
        try:
            while self.connection_status:
                # 接收数据
                tmp_recv_data = (self.request.recv(100000)).decode('utf-8').strip()

                if len(tmp_recv_data) == 0:
                    self.request.send(' '.encode())
                    continue
                else:
                    # 保存接收数据日志
                    if 'SDO_User' not in tmp_recv_data and 'SDO_HeartBeat' not in tmp_recv_data:
                        self.logger_recv.info(tmp_recv_data)
                    else:
                        pass

                    print_log(tmp_recv_data, '接收')

                # 判断接收xml的完整性
                if tmp_recv_data[:5] == '<?xml':
                    recv_data = tmp_recv_data
                else:
                    recv_data += tmp_recv_data

                # 判断xml数据格式是否正确
                if xml_check(recv_data):
                    # 数据存入接收数据队列
                    # print('将数据存入队列')
                    self.queue_recv_data.put(recv_data)
                    recv_data = ''
                else:
                    continue

        except Exception as e:
            self.connection_status = False
            print('处理数据线程结束')
            print(e)

    # 发送数据线程
    def thread_send_data(self):
        while self.connection_status:
            try:
                # 从发送数据队列中取数据
                send_data = self.queue_send_data.get(True, 1)

                # 保存发送数据日志
                if 'SDO_User' not in send_data and 'SDO_HeartBeat' not in send_data:
                    self.logger_send.info(send_data)
                else:
                    pass

                print_log(send_data, '发送')

                # 发送数据
                self.request.send(send_data.encode())

            except Exception as e:
                continue

        print('发送数据线程结束')

    # 处理数据
    def thread_handle_data(self):
        # 创建数据处理对象
        data_handler = DataHandler(self.queue_send_data)

        while self.connection_status:
            try:
                # print(self.connection_status)
                # 从接收数据队列中获取数据
                recv_data = self.queue_recv_data.get(True, 1)

                # 处理数据
                data_handler.xml_parse(recv_data)
                data_handler.data_handle()
            except Exception as e:
                continue

        print('接收数据线程结束')















































