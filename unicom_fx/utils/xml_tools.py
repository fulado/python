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

    operation_dict['@order'] = operation_order
    operation_dict['@name'] = operation_name

    body_dict = collections.OrderedDict()
    body_dict['Operation'] = operation_dict

    return body_dict
