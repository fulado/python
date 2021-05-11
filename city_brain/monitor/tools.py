from odps import ODPS


def get_odps(access_id, access_key, project_name, endpoint):
    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    return o


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
