"""
xml工具
"""
import collections


# 生成返回数据的有序字典
def generate_ordered_dict(operation_order, operation_name, operation_list):
    operation_dict = collections.OrderedDict()
    for ope in operation_list:
        object_dict = collections.OrderedDict()
        object_list = ope[1]
        for obj in object_list:
            object_dict[obj[0]] = obj[1]

        operation_dict[ope[0]] = object_dict

    # operation_dict = list_to_ordered_dict(operation_list)

    operation_dict['@order'] = operation_order
    operation_dict['@name'] = operation_name

    body_dict = collections.OrderedDict()
    body_dict['Operation'] = operation_dict

    return body_dict


# 区域列表的值，转换成有序字典
def list_to_ordered_dict(data_list):
    for data in data_list:
        data_dict_key = data[0]

        if len(data[1]) > 1 and (not isinstance(data[1], str)):
            data_dict_value = list_to_ordered_dict(data[1])
        else:
            data_dict_value = data[1]

        data_dict = collections.OrderedDict()
        data_dict[data_dict_key] = data_dict_value

    return data_dict
