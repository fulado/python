"""
静态数据查询
"""

import time
import random

from server.utils import generate_ordered_dict, xml_construct


class StaticDataSubscribe(object):
    def __init__(self, token, cross_id, obj_name):
        self.seq = ''
        self.token = token
        self.data_type = 'REQUEST'
        self.send_data_xml = ''
        self.cross_id = cross_id    # 相位时需要使用signal_id
        self.obj_name = obj_name

    def create_send_data(self):
        operation_order = '5'
        operation_name = 'Get'

        object_list = [('ObjName', self.obj_name),
                       ('ID', self.cross_id),
                       ('No', ''),
                       ]

        operation_list = [('TSCCmd', object_list),
                          ]

        self.seq = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '000%d%d%d' % (random.randint(0, 9),
                                                                                    random.randint(0, 9),
                                                                                    random.randint(0, 9))

        send_data_dict = generate_ordered_dict(operation_order, operation_name, operation_list)
        self.send_data_xml = xml_construct(send_data_dict, self.seq, self.token, self.data_type)

    # 将数据存入发送数据队列
    def put_send_data_into_queue(self, send_data_queue):
        send_data_queue.put(self.send_data_xml)


if __name__ == '__main__':
    rps = StaticDataSubscribe('123', 'abc', 'SignalControler')
    rps.create_send_data()

    print(rps.send_data_xml)



















