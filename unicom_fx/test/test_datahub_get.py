from datahub import DataHub
from datahub.models import TupleRecord, DatahubException, CursorType

import time
import random

from collections import OrderedDict
from server_2.utils import xml_construct


class DatahubGetter(object):
    def __init__(self, token):
        self.endpoint = 'http://15.74.19.36'
        self.access_id = 'NE5RYcFUSOkzSUQK'
        self.access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
        self.project_name = 'city_brain'
        self.dh = DataHub(self.access_id, self.access_key, self.endpoint, enable_pb=False)

        # topic_name
        self.topic_name_temp_plan = 'ods_rt_signal_tmpplan_config_fengxian'
        self.topic_name_multi_plan = 'ods_signal_multiperiodscenario_config_fengxian'

        # schema
        self.record_schema_temp_plan = self.dh.get_topic(self.project_name, self.topic_name_temp_plan).record_schema
        self.record_schema_multi_plan = self.dh.get_topic(self.project_name, self.topic_name_multi_plan).record_schema

        # timestamp 到毫秒
        self.ts = int(time.time() * 1000) - 60000

        # cursor
        self.cursor_temp_plan = self.dh.get_cursor(self.project_name, self.topic_name_temp_plan,
                                                   '0', CursorType.OLDEST, self.ts).cursor
        self.cursor_multi_plan = self.dh.get_cursor(self.project_name, self.topic_name_multi_plan,
                                                    '0', CursorType.SYSTEM_TIME, self.ts).cursor

        # 信号路口信息
        self.tmp_plan_dict = {}
        self.token = token

    # 订阅临时方案
    def get_temp_plan(self):
        try:
            while True:
                get_result = self.dh.get_tuple_records(self.project_name, self.topic_name_temp_plan, '0',
                                                       self.record_schema_temp_plan, self.cursor_temp_plan, 20)

                # 如果取不到值, 等待1秒钟后再次尝试取值
                if 0 == get_result.record_count:
                    time.sleep(1)
                    # print(self.tmp_plan_dict)
                    continue

                # 根据渠取到的数据构造下发命令的数据, 字典格式
                for record in get_result.records:
                    cross_id = record.get_value('cross_id')

                    if cross_id not in self.tmp_plan_dict.keys():
                        self.tmp_plan_dict[cross_id] = []
                    else:
                        pass

                    stage_no = record.get_value('stage_no')
                    split_time = record.get_value('green')
                    self.tmp_plan_dict[cross_id].append({'stage_no': stage_no, 'split_time': split_time})

                # 游标向下移动
                self.cursor_temp_plan = get_result.next_cursor

                # 构造下发命令的xml格式数据
                self.create_send_data()

        except DatahubException as e:
            print(e)

    # 订阅多时段方案
    def get_multi_plan(self):
        try:
            while True:
                get_result = self.dh.get_tuple_records(self.project_name, self.topic_name_multi_plan, '0',
                                                       self.record_schema_multi_plan, self.cursor_multi_plan, 10)

                for record in get_result.records:
                    print(record)

                if 0 == get_result.record_count:
                    time.sleep(1)

                self.cursor_multi_plan = get_result.next_cursor

        except DatahubException as e:
            print(e)

    # 构造发送命令
    def create_send_data(self):

        for cross_id, plan_list in self.tmp_plan_dict.items():

            split_time_list_element = OrderedDict()
            split_time_list = []
            for plan in plan_list:
                split_time_element = OrderedDict()
                split_time_element['StageNo'] = plan.get('stage_no')
                split_time_element['Split'] = plan.get('split_time')

                split_time_list.append(split_time_element)

            split_time_list_element['SplitTime'] = split_time_list

            temp_plan_param_element = OrderedDict()
            temp_plan_param_element['CrossID'] = cross_id
            temp_plan_param_element['CoordStageNo '] = '0'
            temp_plan_param_element['OffSet'] = '0'
            temp_plan_param_element['SplitTimeList'] = split_time_list_element

            object_element = OrderedDict()
            object_element['TempPlanParam'] = temp_plan_param_element
            object_element['@order '] = '6'
            object_element['@name '] = 'Set'

            operation_element = OrderedDict()
            operation_element['Operation '] = object_element

            send_data_dict = operation_element

            seq = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '000%d%d%d' % (random.randint(0, 9),
                                                                                   random.randint(0, 9),
                                                                                   random.randint(0, 9))

            # send_data_xml = xml_construct(send_data_dict, seq, self.token, 'TempPlanParam')
            send_data_xml = xml_construct(send_data_dict, seq, self.token, 'REQUEST')

            # 数据写入发送队列
            print(send_data_xml)


def get_data_from_datahub():
    endpoint = 'http://15.74.19.36'
    access_id = 'NE5RYcFUSOkzSUQK'
    access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
    project_name = 'city_brain'
    topic_name = 'ods_rt_signal_tmpplan_config_songjiang'

    dh = DataHub(access_id, access_key, endpoint, enable_pb=False)

    # try:
    topic_result = dh.get_topic(project_name, topic_name)
    # print(topic_result)

    tm = int(time.time() * 1000) - 60000
    print(tm)

    cursor_result = dh.get_cursor(project_name, topic_name, '0', CursorType.SYSTEM_TIME, tm)
    cursor = cursor_result.cursor

    while True:
        print(cursor)
        get_result = dh.get_tuple_records(project_name, topic_name, '0', topic_result.record_schema, cursor, 1)
        for record in get_result.records:
            print(record)
        if 0 == get_result.record_count:
            time.sleep(1)
        cursor = get_result.next_cursor

    # except DatahubException as e:
    #     print(e)
        # sys.exit(-1)


if __name__ == '__main__':
    # get_data_from_datahub()

    dg = DatahubGetter('mmmmmmm')
    dg.get_temp_plan()

    # print(dg.tmp_plan_dict)

    # split_time_origin = [(1, 69), (2, 39)]
    # cross_id = '123abc'
    #
    # dg.create_send_data(split_time_origin, cross_id)

















