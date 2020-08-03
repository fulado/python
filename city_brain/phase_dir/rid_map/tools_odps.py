from odps import ODPS


# 写入数据到odps
def write_data_into_odps(table_name, partition, data_list):

    access_id = 'wJGLPrjEt3GCgB2h'
    access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'
    project_name = 'jj_znjt'
    endpoint = 'http://15.74.19.77/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    # 获取表
    t = o.get_table(table_name)

    # t.delete_partition('pt=test', if_exists=True)

    # 写入数据
    with t.open_writer(partition=partition, create_partition=True) as writer:
        records = data_list

        writer.write(records)


# 清空表中的数据
def delete_partition(table_name, partition):

    access_id = 'wJGLPrjEt3GCgB2h'
    access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'
    project_name = 'jj_znjt'
    endpoint = 'http://15.74.19.77/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    # 获取表
    t = o.get_table(table_name)

    try:
        t.delete_partition(partition, if_exists=True)
        print('清除数据成功')
    except Exception as e:
        print(e)
        print('清除数据失败')


if __name__ == '__main__':
    data_list = [['1528I09IMV0', 1, '310000'],
                 ]

    table_name = 'dwd_tfc_ctl_signal_phasedir_baoshan_test'
    partition = 'adcode=310000'

    delete_partition(table_name, partition)
    write_data_into_odps(table_name, partition, data_list)




















