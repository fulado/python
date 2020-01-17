import xml.etree.ElementTree as xml_et
import xmltodict
from pprint import pprint
import json

from server.xml_handler import XmlHandler
from server.sys_data import LoginData, HearBeat, CrossReportCtrl
from server.static_data import SysInfo, LampGroup, LaneParam, PhaseParam
from server.dynamic_data import CrossCycle, CrossStage


def parse_xml(xml_data):
    root = xml_et.fromstring(xml_data)

    version = root.find('Version').text
    token = root.find('Token').text
    client_address = root.find('From').text
    data_type = root.find('Type').text
    seq = root.find('Seq').text

    body = root.find('Body')

    operation = body.find('Operation')
    operation_name = operation.attrib.get('name', '')

    print(operation_name)

    obj = operation[0]

    print(obj.tag)
    #
    # username = obj.find('UserName').text
    # print(username)
    #
    # password = obj.find('Pwd').text
    # print(password)

    data = xmltodict.parse(xml_data)
    # data = json.loads(json.dumps(data))
    print(data.get('Message'))





# def get_child_element(element, data):
#     data = {element.tag: element.text}
#
#     for child in element:
#         if child is not None:
#             print(child.tag, child.attrib, child.text)
#             get_child_element(child)
#         else:
#             return
        


if __name__ == '__main__':
    xml_data = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>451e8ad42dfca3b1a72880b118ac35fda93af922</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200115171602000001</Seq><Body><Operation name="Get" order="5"><SysInfo><SysName>CSTCP4.0信号控制系统</SysName><SysVersion>1.0</SysVersion><Supplier>宝康</Supplier><RegionIDList><RegionID>310120000</RegionID></RegionIDList><SignalControlerIDList><SignalControlerID>31012000000000066</SignalControlerID><SignalControlerID>31012000000000064</SignalControlerID><SignalControlerID>31012000000000065</SignalControlerID><SignalControlerID>31012000000000067</SignalControlerID><SignalControlerID>31012000000000068</SignalControlerID><SignalControlerID>31012000000000069</SignalControlerID><SignalControlerID>31012000000000002</SignalControlerID><SignalControlerID>31012000000000001</SignalControlerID><SignalControlerID>31012000000000005</SignalControlerID><SignalControlerID>31012000000000006</SignalControlerID><SignalControlerID>31012000000000007</SignalControlerID><SignalControlerID>31012000000000008</SignalControlerID><SignalControlerID>31012000000000009</SignalControlerID><SignalControlerID>31012000000000011</SignalControlerID><SignalControlerID>31012000000000012</SignalControlerID><SignalControlerID>31012000000097055</SignalControlerID><SignalControlerID>31012000000000015</SignalControlerID><SignalControlerID>31012000000000019</SignalControlerID><SignalControlerID>31012000000000021</SignalControlerID><SignalControlerID>31012000000000022</SignalControlerID><SignalControlerID>31012000000000023</SignalControlerID><SignalControlerID>31012000000000024</SignalControlerID><SignalControlerID>31012000000000025</SignalControlerID><SignalControlerID>31012000000000026</SignalControlerID><SignalControlerID>31012000000000027</SignalControlerID><SignalControlerID>31012000000000030</SignalControlerID><SignalControlerID>31012000000000032</SignalControlerID><SignalControlerID>31012000000000033</SignalControlerID><SignalControlerID>31012000000000035</SignalControlerID><SignalControlerID>31012000000000036</SignalControlerID><SignalControlerID>31012000000000038</SignalControlerID><SignalControlerID>31012000000000013</SignalControlerID><SignalControlerID>31012000000000014</SignalControlerID><SignalControlerID>31012000000000016</SignalControlerID><SignalControlerID>31012000000000018</SignalControlerID><SignalControlerID>31012000000000028</SignalControlerID><SignalControlerID>31012000000000029</SignalControlerID><SignalControlerID>31012000000000031</SignalControlerID><SignalControlerID>31012000000000034</SignalControlerID><SignalControlerID>31012000000000037</SignalControlerID><SignalControlerID>31012000000000039</SignalControlerID><SignalControlerID>31012000000000040</SignalControlerID><SignalControlerID>31012000000000041</SignalControlerID><SignalControlerID>31012000000000042</SignalControlerID><SignalControlerID>31012000000000043</SignalControlerID><SignalControlerID>31012000000000044</SignalControlerID><SignalControlerID>31012000000000017</SignalControlerID><SignalControlerID>31012000000000045</SignalControlerID><SignalControlerID>31012000000000046</SignalControlerID><SignalControlerID>31012000000000047</SignalControlerID><SignalControlerID>31012000000000003</SignalControlerID><SignalControlerID>31012000000000004</SignalControlerID><SignalControlerID>31012000000000010</SignalControlerID><SignalControlerID>31012000000000020</SignalControlerID><SignalControlerID>31012000000000048</SignalControlerID><SignalControlerID>31012000000000049</SignalControlerID><SignalControlerID>31012000000000050</SignalControlerID><SignalControlerID>31012000000000051</SignalControlerID><SignalControlerID>31012000000000052</SignalControlerID><SignalControlerID>31012000000000053</SignalControlerID><SignalControlerID>31012000000000054</SignalControlerID><SignalControlerID>31012000000000055</SignalControlerID><SignalControlerID>31012000000000056</SignalControlerID><SignalControlerID>31012000000000057</SignalControlerID><SignalControlerID>31012000000000058</SignalControlerID><SignalControlerID>31012000000000059</SignalControlerID><SignalControlerID>31012000000000060</SignalControlerID><SignalControlerID>31012000000000061</SignalControlerID><SignalControlerID>31012000000000062</SignalControlerID><SignalControlerID>31012000000000063</SignalControlerID></SignalControlerIDList></SysInfo></Operation></Body></Message>
    """

    # parse_xml(xml_data.strip())

    xml_handler = XmlHandler()
    xml_handler.xml_parse(xml_data.strip())


    # print(xml_handler.object_type)
    # print(xml_handler.request_data_dict)

    # # 登录
    # login_data = LoginData(xml_handler.request_data_dict)
    # login_data.get_user_info()
    # login_data.set_response_data()
    #
    # xml_handler.xml_construct(login_data.response_date, login_data.data_type, login_data.token)
    #
    # # 心跳
    # heart_beat = HearBeat(xml_handler.request_data_dict)
    # heart_beat.set_response_data()
    #
    # xml_handler.xml_construct(heart_beat.response_date, heart_beat.data_type)
    #
    # # 系统参数请求
    # sys_info = SysInfo()
    # sys_info.set_request_data()
    # xml_handler.xml_construct(sys_info.request_data, sys_info.data_type)
    # sys_info.parse_response_data(xml_handler.request_data_dict)

    # 路口周期
    # cross_cycle = CrossCycle()
    # cross_cycle.parse_data(xml_handler.request_data_dict)
    # cross_cycle.save_data()

    # 路口周期
    # CrossStage = CrossStage()
    # CrossStage.parse_data(xml_handler.request_data_dict)
    # CrossStage.save_data()

    # 订阅数据
    cross_cycle = CrossReportCtrl('CrossCycle')
    cross_cycle.get_cross_id_list()
    cross_cycle.set_response_data()

    xml_handler.xml_construct(cross_cycle.response_data, cross_cycle.data_type, '', cross_cycle.seq)


    #
    # sys_info = PhaseParam('123')
    # sys_info.set_request_data()
    # xml_handler.xml_construct(sys_info.request_data, sys_info.data_type)
    # print(xml_handler.response_data_xml)
    # sys_info.parse_response_data(xml_handler.request_data_dict)
    # sys_info.save_data_to_file()


    # 系统参数返回
    print(xml_handler.response_data_xml)

