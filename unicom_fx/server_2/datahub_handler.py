"""
datahub操作
"""
from datahub import DataHub
from datahub.models import TupleRecord, DatahubException


class DatahubHandler(object):
    def __init__(self):
        self.endpoint = 'http://15.74.19.36'
        self.access_id = 'NE5RYcFUSOkzSUQK'
        self.access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
        self.project_name = 'city_brain'
        self.dh = DataHub(self.access_id, self.access_key, self.endpoint, enable_pb=False)

    # 发布数据
    def put_data(self, topic_name, data_list):
        try:

            # block等待所有shard状态ready
            self.dh.wait_shards_ready(self.project_name, topic_name)

            topic_result = self.dh.get_topic(self.project_name, topic_name)

            record_schema = topic_result.record_schema

            records = []

            for data in data_list:
                record = TupleRecord(schema=record_schema)
                record.values = data
                records.append(record)

            self.dh.put_records(self.project_name, topic_name, records)

        except DatahubException as e:
            print(e)
























