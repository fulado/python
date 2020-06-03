"""
心跳
"""

from server_sj.utils import generate_ordered_dict, xml_construct


class SdoHeartBeat(object):
    def __init__(self, seq, token):
        self.seq = seq
        self.token = token
        self.data_type = 'PUSH'
        self.send_data_xml = ''

    def create_send_data(self):
        operation_list = [('SDO_HeartBeat', [])]
        operation_order = '7'
        operation_name = 'notify'

        send_data_dict = generate_ordered_dict(operation_order, operation_name, operation_list)
        self.send_data_xml = xml_construct(send_data_dict, self.seq, self.token, self.data_type)

    # 将数据存入发送数据队列
    def put_send_data_into_queue(self, send_data_queue):
        send_data_queue.put(self.send_data_xml)







































