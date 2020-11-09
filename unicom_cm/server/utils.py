"""
工具类
"""
import collections
import xmltodict
import time
import logging

from xml.sax import parseString as ps
from xml.sax.handler import ContentHandler


# 保存数据日志，暂时在屏幕上打印结果
def create_logger(activation):

    if activation == 'recv':
        logger = logging.getLogger('recv')
    elif activation == 'send':
        logger = logging.getLogger('send')
    else:
        logger = logging.getLogger(__name__)

    logger.setLevel(level=logging.INFO)

    log_handler = logging.FileHandler("../log/%s.txt" % time.strftime('%Y-%m-%d', time.localtime()))
    log_handler.setLevel(logging.INFO)

    if activation == 'recv':
        formatter = logging.Formatter(fmt='\n%(asctime)s recv data\n%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    elif activation == 'send':
        formatter = logging.Formatter(fmt='\n%(asctime)s send data\n%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter(fmt='\n%(asctime)s/n%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)

    return logger


# 打印数据
def print_log(data_content, activation):

    print('%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('==========================%s数据==========================' % activation)
    print(data_content)
    print('==========================%s完毕==========================\n\n' % activation)


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


# str类型转换为int类型
def str_to_int(value):
    try:
        val = int(float(value))
    except ValueError:
        val = 0

    return val


if __name__ == '__main__':
    # data_string = 'aaa'
    # print_log(data_string, '接收')

    xml_string = '<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>8C9518A7AD2CB43B01F3B0EEBF6DA86287F55C6B</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200908060020000001</Seq><Body><Operation name="Notify" order="1"><CrossCycle><CrossID>31012000000065</CrossID><StartTime>2020-09-08 06:00:20</StartTime><LastCycleLen>140.0</LastCycleLen><CurCycleLen>140.0</CurCycleLen><CurCycleRemainLen>140.0</CurCycleRemainLen></CrossCycle></Operation></Body></Message><?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>8C9518A7AD2CB43B01F3B0EEBF6DA86287F55C6B</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200908055841000040</Seq><Body><Operation name="Set" order="6"><TempPlanParam><CrossID>31012000000052</CrossID><CoordStageNo>3</CoordStageNo><OffSet>37</OffSet><EndTime>2020-09-08 07:29:00</EndTime><SplitTimeList><SplitTime><StageNo>1</StageNo><Green>86</Green></SplitTime><SplitTime><StageNo>2</StageNo><Green>56</Green></SplitTime></SplitTimeList></TempPlanParam></Operation></Body></Message>'
    res = xml_check(xml_string)

    print(res)





