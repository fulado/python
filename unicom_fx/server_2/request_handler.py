import time

from socketserver import BaseRequestHandler
from multiprocessing import Queue
from threading import Thread
from .utils import save_log, xml_check


# BaseRequestHandler子类
class MyRequestHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(MyRequestHandler, self).__init__(request, client_address, server)
        self.queue_request_data = Queue(50)  # 接收数据队列
        self.queue_response_data = Queue(50)  # 发送数据队列

    def setup(self):
        print('%s : 连接建立, %s:%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                                    self.client_address[0], self.client_address[1]))

    def handle(self):
        # 创建并启动接收数据线程
        t_recv_data = Thread(target=self.thread_recv_data())
        t_recv_data.start()

        # 创建并启动发送数据线程
        t_send_data = Thread(target=self.thread_send_data())
        t_send_data.start()

    def finish(self):
        print('%s : 连接关闭' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # 接收数据线程
    def thread_recv_data(self):
        request_data = ''
        while True:
            try:
                # 接收数据
                tmp_request_data = (self.request.recv(100000)).decode('utf-8')

                # 保存接收数据日志
                save_log(tmp_request_data, '接收')

                # 判断接收xml的完整性
                if tmp_request_data[:5] == '<?xml':
                    request_data = tmp_request_data
                else:
                    request_data += tmp_request_data

                # 判断xml数据格式是否正确
                if xml_check(request_data):
                    # 数据存入接收数据队列
                    self.queue_request_data.put(request_data)
                    request_data = ''
                else:
                    continue

            except Exception as e:
                print(e)

    # 发送数据线程
    def thread_send_data(self):
        while True:
            try:
                # 从发送数据队列中取数据
                response_data = self.queue_response_data.get()

                # 保存发送数据日志
                save_log(response_data, '发送')

                # 发送数据
                self.request.send(response_data.encode())

            except Exception as e:
                print(e)

    # 处理数据
    def thread_handle_data(self):
        # 从接收数据队列中获取数据

        # 处理数据

        # 将发送数据放入发送数据队列


















