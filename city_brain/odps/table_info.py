from pprint import pprint

from odps import ODPS
from odps.df import DataFrame


def get_tables(o):
    """查询项目下的所有表"""
    return [table.name for table in o.list_tables()]


def get_table_size(o, table_name):
    """根据表名查询表大小"""
    sql = 'desc ' + table_name

    with o.execute_sql(sql).open_reader() as reader:
        res = reader.raw

        start_pos = res.find('Size: ')
        res = res[start_pos + 6:]

        stop_pos = res.find(' ')
        table_size = res[:stop_pos]

        return table_size


def get_tables_info(o):
    """获取表名和相应的"""
    table_list = get_tables(o)

    table_size_list = []
    for table_name in table_list:
        table_size = get_table_size(o, table_name)

        table_size_list.append({'table_name': table_name,
                                'table_size': table_size})

        print(table_name, table_size)
    return table_size_list


def get_table_frame(o, table_name):
    """获取table的frame信息, 测试用"""
    sql = 'desc ' + table_name
    with o.execute_sql(sql).open_reader() as reader:
        res = reader.raw
        print(res)

        start_pos = res.find('Size: ')
        res = res[start_pos+6:]

        stop_pos = res.find(' ')
        res = res[:stop_pos]
        print(res)


if __name__ == '__main__':
    access_id = 'NE5RYcFUSOkzSUQK'
    access_key = 'gmQxEPpXfYXd7BCwQQUM3OxvpmZwRn'
    project_name = 'city_brain'
    endpoint = 'http://service.cn-shanghai-shga-d01.odps.ops.ga.sh/api'
    endpoint = 'http://15.74.19.77/api'

    o = ODPS(access_id=access_id,
             secret_access_key=access_key,
             project=project_name,
             endpoint=endpoint
             )

    # table = DataFrame(o.get_table('dim_signaloptim_inter_info_chongming'))

    # table_list = get_tables(o)

    # get_table_frame(o, 'dim_signaloptim_inter_info_baoshan')

    tables_info = get_tables_info(o)

    # pprint(tables_info)







