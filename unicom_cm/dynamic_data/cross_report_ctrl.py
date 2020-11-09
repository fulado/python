"""
路口实时状态订阅
"""

import time
import random

from collections import OrderedDict
from server.utils import xml_construct


class CrossReportCtrl(object):
    def __init__(self, token):
        self.data_type = 'REQUEST'
        self.object_type = 'CrossReportCtrl'
        self.cross_id_list = []
        self.send_data_xml = ''
        self.seq = ''
        self.token = token

    # 获取路口id列表
    def get_cross_id_list(self):
        file = open('../data/cross_list.txt', 'r')
        self.cross_id_list = []

        try:
            for line in file.readlines():
                self.cross_id_list.append(line.strip())

        except Exception as e:
            print(e)
        finally:
            file.close()

    # 设定路口id
    def set_cross_id_list(self, cross_id_list):
        self.cross_id_list = cross_id_list

    def create_send_data(self, data_type_name):
        cross_id_list_element = OrderedDict()
        cross_id_list_element['CrossID'] = self.cross_id_list

        cross_report_ctrl_element = OrderedDict()
        cross_report_ctrl_element['Cmd'] = 'Start'
        cross_report_ctrl_element['Type'] = data_type_name
        cross_report_ctrl_element['CrossIDList'] = cross_id_list_element

        object_element = OrderedDict()
        object_element[self.object_type] = cross_report_ctrl_element
        object_element['@order '] = '6'
        object_element['@name '] = 'Set'

        operation_element = OrderedDict()
        operation_element['Operation '] = object_element

        send_data_dict = operation_element

        self.seq = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '000%d%d%d' % (random.randint(0, 9),
                                                                                    random.randint(0, 9),
                                                                                    random.randint(0, 9))

        self.send_data_xml = xml_construct(send_data_dict, self.seq, self.token, self.data_type)

    # 将数据存入发送数据队列
    def put_send_data_into_queue(self, send_data_queue):
        send_data_queue.put(self.send_data_xml)


# 测试
# if __name__ == '__main__':
#     crt = CrossReportCtrl('123')
#     crt.get_cross_id_list()
#     crt.create_send_data('CrossCycle')
#
#     print(crt.send_data_xml)
























