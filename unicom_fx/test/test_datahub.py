from datahub import DataHub
from datahub.models import RecordType, TupleRecord, DatahubException

import sys


access_id = 'NE5RYcFUSOkzSUQK'
access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'

endpoint = 'http://15.74.19.36'

project_name = 'city_brain'
topic_name = 'ods_rt_signal_tmpplan_result_fengxian'

dh = DataHub(access_id, access_key, endpoint, enable_pb=False)

shard_result = dh.list_shard(project_name, topic_name)
shards = shard_result.shards
shard_id = shards[0].shard_id
# print(shards)


# print("=======================================\n\n")
# for shard in shard_result.shards:
#     print(shard)
# print("=======================================\n\n")


# 发布数据
def put_data():
    try:
        # block等待所有shard状态ready
        # dh.wait_shards_ready(project_name, topic_name)
        #
        # print("shards all ready!!!")
        # print("=======================================\n\n")
        topic_result = dh.get_topic(project_name, topic_name)
        # # print(topic_result)
        #
        # if topic_result.record_type != RecordType.TUPLE:
        #     print("topic type illegal!")
        #     sys.exit(-1)
        # print("=======================================\n\n")

        record_schema = topic_result.record_schema
        # print(record_schema)

        records = []

        record = TupleRecord(schema=record_schema)
        record.values = ['31012000000042', '2020-06-15 18:00:00', 1, '2020-06-16 17:45:00', '2020-06-16 17:45:00', "{'CrossID': '31012000000042', 'EndTime': '2020-06-15 18:00:00', 'CoordStageNo': '7', 'OffSet': '3', 'SplitTimeList': [{'stageNo': '7', 'Green': '36'}, {'stageNo': '8', 'Green': '79'}, {'stageNo': '9', 'Green': '37'}]}"]
        # record.shard_id = 0
        records.append(record)

        # # print(project_name)
        # # print(topic_name)
        # # print(shard_id)
        # # print(records)
        #
        put_result = dh.put_records(project_name, topic_name, records)

        print(put_result)
        # print("put tuple %d records, failed count: %d" % (len(records), put_result.failed_record_count))
        # # failed_record_count如果大于0最好对failed record再进行重试
        # print("=======================================\n\n")

    except DatahubException as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    put_data()






