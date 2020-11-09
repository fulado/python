from datahub import DataHub
from datahub.models import DatahubException, CursorType

import time
import random

from collections import OrderedDict
from server.utils import xml_construct


class TempPlan(object):
    def __init__(self, token, send_data_queue):
        self.endpoint = 'http://15.74.19.36'
        self.access_id = 'NE5RYcFUSOkzSUQK'
        self.access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
        self.project_name = 'city_brain'
        self.dh = DataHub(self.access_id, self.access_key, self.endpoint, enable_pb=False)

        # topic_name
        self.topic_name_temp_plan = 'ods_rt_signal_tmpplan_config_fengxian'
        self.record_schema_temp_plan = None
        self.cursor_temp_plan = None

        # 信号路口信息
        self.tmp_plan_dict = {}
        self.token = token

        # 命令数据xml
        self.send_data_xml = ''

        # 发送数据队列
        self.send_data_queue = send_data_queue

    # 链接datahub
    def connect_datahub(self):

        # schema
        self.record_schema_temp_plan = self.dh.get_topic(self.project_name, self.topic_name_temp_plan).record_schema

        # timestamp 到毫秒
        ts = int(time.time() * 1000) - 60000  # 此处因为系统时间不准, 把时间提前一分钟

        # cursor
        self.cursor_temp_plan = self.dh.get_cursor(self.project_name, self.topic_name_temp_plan,
                                                   '0', CursorType.SYSTEM_TIME, ts).cursor

    # 订阅临时方案
    def get_temp_plan(self):
        try:
            get_result = self.dh.get_tuple_records(self.project_name, self.topic_name_temp_plan, '0',
                                                   self.record_schema_temp_plan, self.cursor_temp_plan, 20)

            # 如果取不到值, 等待1秒钟后再次尝试取值
            if 0 == get_result.record_count:
                time.sleep(1)
                # print(self.tmp_plan_dict)
                return

            # 根据渠取到的数据构造下发命令的数据, 字典格式
            for record in get_result.records:
                cross_id = record.get_value('cross_id')

                if cross_id not in self.tmp_plan_dict.keys():
                    self.tmp_plan_dict[cross_id] = []
                else:
                    pass

                stage_no = record.get_value('stage_no')
                split_time = record.get_value('green')
                end_time = record.get_value('end_time')
                self.tmp_plan_dict[cross_id].append({'stage_no': stage_no,
                                                     'split_time': split_time,
                                                     'end_time': end_time})

            # 游标向下移动
            self.cursor_temp_plan = get_result.next_cursor

            # 构造下发命令的xml格式数据
            self.create_send_data()

            # 将下发命令的xml数据放入队列
            self.send_data_queue.put(self.send_data_xml)
            # print(self.send_data_xml)

            # 清空tmp_plan_dict
            self.tmp_plan_dict = {}

        except DatahubException as e:
            print(e)

    # 构造发送命令
    def create_send_data(self):

        for cross_id, plan_list in self.tmp_plan_dict.items():

            split_time_list_element = OrderedDict()
            split_time_list = []

            end_time = '0'

            is_cancel_cmd = False

            for plan in plan_list:
                split_time_element = OrderedDict()
                stage_no = plan.get('stage_no')
                split_time = plan.get('split_time')

                if stage_no == 0 and split_time == 0:
                    is_cancel_cmd = True
                else:
                    split_time_element['StageNo'] = stage_no
                    split_time_element['Green'] = split_time

                    split_time_list.append(split_time_element)

                    end_time = plan.get('end_time', '0')

            if is_cancel_cmd:
                temp_plan_param_element = OrderedDict()
                temp_plan_param_element['CrossID'] = cross_id
                temp_plan_param_element['Type'] = '1'
                temp_plan_param_element['Entrance'] = '8'
                temp_plan_param_element['Exit'] = '8'

                object_element = OrderedDict()
                object_element['UnLockFlowDirection'] = temp_plan_param_element
            else:
                split_time_list_element['SplitTime'] = split_time_list

                temp_plan_param_element = OrderedDict()
                temp_plan_param_element['CrossID'] = cross_id
                temp_plan_param_element['CoordStageNo'] = '0'
                temp_plan_param_element['OffSet'] = '0'
                temp_plan_param_element['EndTime'] = end_time
                temp_plan_param_element['SplitTimeList'] = split_time_list_element

                object_element = OrderedDict()
                object_element['TempPlanParam'] = temp_plan_param_element

            object_element['@order'] = '6'
            object_element['@name'] = 'Set'

            operation_element = OrderedDict()
            operation_element['Operation'] = object_element

            send_data_dict = operation_element

            seq = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '000%d%d%d' % (random.randint(0, 9),
                                                                                   random.randint(0, 9),
                                                                                   random.randint(0, 9))

            self.send_data_xml = xml_construct(send_data_dict, seq, self.token, 'REQUEST')

            # print(send_data_xml)




















