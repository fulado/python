from datahub import DataHub
from datahub.models import TupleRecord, DatahubException, CursorType

import time
import sys


class DatahubGetter(object):
    def __init__(self):
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
                                                   '0', CursorType.SYSTEM_TIME, self.ts).cursor
        self.cursor_multi_plan = self.dh.get_cursor(self.project_name, self.topic_name_multi_plan,
                                                    '0', CursorType.SYSTEM_TIME, self.ts).cursor

    # 订阅临时方案
    def get_temp_plan(self):
        try:
            while True:
                get_result = self.dh.get_tuple_records(self.project_name, self.topic_name_temp_plan, '0',
                                                       self.record_schema_temp_plan, self.cursor_temp_plan, 10)

                for record in get_result.records:
                    print(record)

                if 0 == get_result.record_count:
                    time.sleep(1)

                self.cursor_temp_plan = get_result.next_cursor

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

    dg = DatahubGetter()
    dg.get_temp_plan()


















