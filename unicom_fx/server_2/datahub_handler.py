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

        # topic_name
        self.topic_lamp_param = 'ods_signal_lightset_froad_rltn_gb1049_fengxian'
        self.topic_lane_param = 'ods_signal_froad_info_gb1049_fengxian'
        self.topic_stage_param = 'ods_signal_stage_info_gb1049_fengxian'
        self.topic_plan_param = 'ods_signal_timeplan_config_gb1049_fengxian'
        self.topic_cross_cycle = 'ods_signal_cycle_rt_gb1049_fengxian'
        self.topic_cross_stage = 'ods_signal_stage_rt_gb1049_fengxian'

    # 发布数据
    def put_data(self, obj_name, data_list):

        if obj_name == 'LampParam':
            topic_name = self.topic_lamp_param
        elif obj_name == 'LaneParam':
            topic_name = self.topic_lane_param
        elif obj_name == 'StageParam':
            topic_name = self.topic_stage_param
        elif obj_name == 'PlanParam':
            topic_name = self.topic_plan_param
        elif obj_name == 'CrossCycle':
            topic_name = self.topic_cross_cycle
        elif obj_name == 'CrossStage':
            topic_name = self.topic_cross_stage
        else:
            return

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
























