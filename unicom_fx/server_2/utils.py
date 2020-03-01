"""
工具类
"""
import collections
import xmltodict

from xml.sax import parseString as ps
from xml.sax.handler import ContentHandler


# 保存数据日志，暂时在屏幕上打印结果
def save_log(data_content, activation):
    print()
    print('==========================%s数据==========================' % activation)
    print(data_content)
    print('==========================%s完毕==========================' % activation)
    print()


# 验证xml字符是否正确
def xml_check(xml_string):

    try:
        ps(xml_string, ContentHandler())
        return True
    except Exception as e:
        print('xml格式错误')
        print(e)
        return False


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


# 构造返回xml
def xml_construct(send_data_dict, seq='', token='', data_type='RESPONSE'):
    message = collections.OrderedDict()
    message['Version'] = '1.0'
    message['Token'] = token

    # 构造From标签中的内容
    from_address = collections.OrderedDict()
    from_address['Sys'] = 'TICP'
    from_address['SubSys'] = ''
    from_address['Instance'] = ''

    from_element = collections.OrderedDict()
    from_element['Address'] = from_address
    message['From'] = from_element

    # 构造To标签中的内容
    to_address = collections.OrderedDict()
    to_address['Sys'] = 'UTCS'
    to_address['SubSys'] = ''
    to_address['Instance'] = ''

    to_element = collections.OrderedDict()
    to_element['Address'] = to_address
    message['To'] = to_element

    message['Type'] = data_type
    message['Seq'] = seq
    message['Body'] = send_data_dict

    response_data_dict = collections.OrderedDict()
    response_data_dict['Message'] = message

    return xmltodict.unparse(response_data_dict)


if __name__ == '__main__':
    data_string = 'bbb'
    res = xml_check(data_string)

    print(res)



