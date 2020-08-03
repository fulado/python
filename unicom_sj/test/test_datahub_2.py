import sys
import traceback
from datahub import DataHub
from datahub.exceptions import ResourceExistException
from datahub.models import FieldType, RecordSchema, TupleRecord, BlobRecord, CursorType, RecordType, DatahubException

access_id = 'NE5RYcFUSOkzSUQK'
access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'

endpoint = 'http://15.74.19.36'

dh = DataHub(access_id, access_key, endpoint, enable_pb=False)

project_name = 'city_brain'
comment = 'test'
topic_name = "tuple_topic"


def create_topic():

    shard_count = 3
    life_cycle = 7
    record_schema = RecordSchema.from_lists(
        ['bigint_field', 'string_field', 'double_field', 'bool_field', 'time_field'],
        [FieldType.BIGINT, FieldType.STRING, FieldType.DOUBLE, FieldType.BOOLEAN, FieldType.TIMESTAMP])
    try:
        dh.create_tuple_topic(project_name, topic_name, shard_count, life_cycle, record_schema, comment)
        print("create tuple topic success!")
        print("=======================================\n\n")
    except ResourceExistException:
        print("topic already exist!")
        print("=======================================\n\n")
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(-1)


def put_data():
    try:
        # block等待所有shard状态ready
        dh.wait_shards_ready(project_name, topic_name)
        print("shards all ready!!!")
        print("=======================================\n\n")
        topic_result = dh.get_topic(project_name, topic_name)
        print(topic_result)
        if topic_result.record_type != RecordType.TUPLE:
            print("topic type illegal!")
            sys.exit(-1)
        print("=======================================\n\n")
        record_schema = topic_result.record_schema
        records0 = []
        record0 = TupleRecord(schema=record_schema, values=[1, 'yc1', 10.01, True, 1455869335000000])
        record0.shard_id = '0'
        record0.put_attribute('AK', '47')
        records0.append(record0)
        record1 = TupleRecord(schema=record_schema)
        record1.set_value('bigint_field', 2)
        record1.set_value('string_field', 'yc2')
        record1.set_value('double_field', None)
        record1.set_value('bool_field', False)
        record1.set_value('time_field', 1455869335000011)
        record1.hash_key = '4FFFFFFFFFFFFFFD7FFFFFFFFFFFFFFD'
        records0.append(record1)
        record2 = TupleRecord(schema=record_schema)
        record2.set_value(0, 3)
        record2.set_value(1, 'yc3')
        record2.set_value(2, 1.1)
        record2.set_value(3, False)
        record2.set_value(4, 1455869335000011)
        record2.attributes = {'key': 'value'}
        record2.partition_key = 'TestPartitionKey'
        records0.append(record2)
        put_result = dh.put_records(project_name, topic_name, records0)
        print(put_result)
        print("put tuple %d records, failed count: %d" % (len(records0), put_result.failed_record_count))
        # failed_record_count如果大于0最好对failed record再进行重试
        print("=======================================\n\n")
    except DatahubException as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    put_data()

