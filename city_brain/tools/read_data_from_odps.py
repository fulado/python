from odps import ODPS
from odps.df import DataFrame
from datahub import DataHub
from datahub.models import RecordType, TupleRecord, DatahubException

import time


def get_odps(access_id, access_key, project_name, endpoint):
    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    return o


def get_table(o, table_name):
    return DataFrame(o.get_table(table_name))


def excute_sql(o, sql):
    reader = o.execute_sql(sql).open_reader()

    data_list = []
    for record in reader:
        # print(record)

        # flow_data = {'stat_time': record.stat_time,
        #              'inter_id': record.inter_id,
        #              'f_rid': record.f_rid,
        #              't_rid': record.t_rid,
        #              'turn_dir_no': record.turn_dir_no,
        #              'step_index': record.step_index,
        #              'multi_type': record.multi_type,
        #              'flow': record.flow,
        #              'reliability_code': record.reliability_code,
        #              'dt': record.dt,
        #              'tp': record.tp,
        #              'data_version': record.data_version,
        #              'adcode': record.adcode,
        #              }

        flow_data = [record.stat_time,
                     record.inter_id,
                     record.f_rid,
                     record.t_rid,
                     record.turn_dir_no,
                     record.step_index,
                     record.multi_type,
                     record.flow,
                     record.reliability_code,
                     record.dt,
                     record.tp,
                     record.data_version,
                     record.adcode
                     ]

        data_list.append(flow_data)

    # print(data_list)
    return data_list


def get_data_from_odps_by_sql(o, sql):
    """
    执行sql, 从odps查询数据
    :param o: odps对象
    :param sql: sql语句
    :return:
    """
    reader = o.execute_sql(sql).open_reader()

    data_list = []
    for record in reader:
        data = []

        for field in record:
            data.append(field)

        data_list.append(data)

    return data_list


def put_data(data_list):
    dh_access_id = 'wJGLPrjEt3GCgB2h'
    dh_access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'

    # dh_endpoint = 'http://15.74.19.36'
    # dh_endpoint = 'http://101.89.99.42'
    dh_endpoint = 'http://datahub.cn-shanghai-shga-d01.dh.alicloud.ga.sh'

    dh_project_name = 'city_brain_rid_dev'
    dh_topic_name = 'dws_tfc_trl_interfrid_tp_multiflow_rt'

    dh = DataHub(dh_access_id, dh_access_key, dh_endpoint, enable_pb=False)

    # shard_result = dh.list_shard(dh_project_name, dh_topic_name)
    # shards = shard_result.shards
    # shard_id = shards[0].shard_id

    try:

        topic_result = dh.get_topic(dh_project_name, dh_topic_name)

        record_schema = topic_result.record_schema
        # print(record_schema)

        records = []

        for data in data_list:
            # print(data)
            record = TupleRecord(schema=record_schema)
            record.values = data

            records.append(record)

        put_result = dh.put_records(dh_project_name, dh_topic_name, records)

        print(put_result)

        # print("put tuple %d records, failed count: %d" % (len(records), put_result.failed_record_count))
        # # failed_record_count如果大于0最好对failed record再进行重试
        # print("=======================================\n\n")

    except DatahubException as e:
        print(e)


if __name__ == '__main__':
    access_id = 'wJGLPrjEt3GCgB2h'
    access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'
    # project_name = 'jj_znafaqglxt2'
    project_name = 'jj_znjt'
    endpoint = 'http://15.74.19.77/api'

    # table_name = 'dws_tfc_trl_interfrid_tp_multiflow_rt_ly'

    odps = get_odps(access_id, access_key, project_name, endpoint)
    # table = get_table(odps, table_name)

    # sql = """select * from dws_tfc_trl_interfrid_tp_multiflow_rt_ly"""

    # while True:
    #     flow_data_list = excute_sql(odps, sql)
    #     put_data(flow_data_list)
    #
    #     time.sleep(300)

    sql = """
            select DISTINCT t1.cust_devc_id as radar_id, t3.cust_devc_id as scats_id, t2.inter_name from dwd_tfc_rltn_devc_lane_qianxun_xuhui t1
            join jj_znafaqglxt2.dwd_tfc_bas_rdnet_inter_info t2 on t1.inter_id=t2.inter_id
            join dwd_tfc_rltn_devc_lane_qianxun_xuhui t3 on t1.inter_id=t3.inter_id and t3.qx_type_no='7' and t3.cust_devc_id not in ('xh01', 'xh02')
            where t1.qx_type_no='12' and t1.cust_devc_id not in (
                select DISTINCT radar_id from ods_rt_radar_lane_statparameter_image_dianke
                where dt=to_char(getdate(), 'yyyymmdd') and radar_id like '310104%'
            )
            order by radar_id;
        """

    res = get_data_from_odps_by_sql(odps, sql)

    print(res)
