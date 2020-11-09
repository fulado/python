from odps import ODPS
import time


# 写入数据
def write_data_into_odps():
    access_id = 'wJGLPrjEt3GCgB2h'
    access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'
    project_name = 'jj_znjt'
    endpoint = 'http://15.74.19.77/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    table_name = 'python_tongren'
    partition = 'dt=20200814'

    # 获取表
    t = o.get_table(table_name)

    # t.delete_partition('pt=test', if_exists=True)
    # 获取写入数据
    data_list = get_data_list()

    # 写入数据
    with t.open_writer(partition=partition, create_partition=True) as writer:
        records = data_list

        writer.write(records)


# 生成数据
def get_data_list():
    data = ['佟仁', '0027015934', int(time.time()), '20200814']

    data_list = []
    for i in range(30):
        data_list.append(data)

    return data_list


# 读出数据
def read_data_from_odps():
    access_id = 'wJGLPrjEt3GCgB2h'
    access_key = 'SJcsN7acOaCsaAYicrX0iU8l72x9GZ'
    project_name = 'jj_znjt'
    endpoint = 'http://15.74.19.77/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    sql = 'select * from python_tongren;'

    reader = o.execute_sql(sql).open_reader()

    for record in reader:
        print(record)


if __name__ == '__main__':
    write_data_into_odps()

    read_data_from_odps()

