import xml.etree.ElementTree as xml_et
import xmltodict
from pprint import pprint
import json

from server.xml_handler import XmlHandler
from server.sys_data import LoginData, HearBeat, CrossReportCtrl
from server.static_data import SysInfo, LampGroup
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
<?xml version="1.0" encoding="UTF-8"?>
<Message>
  <Version>1.1</Version>
  <Token></Token>
  <From>
    <Address>
      <Sys>UTCS</Sys>
      <SubSys/>
      <Instance/>
    </Address>
  </From>
  <To>
    <Address>
      <Sys>TICP</Sys>
      <SubSys/>
      <Instance/>
    </Address>
  </To>
  <Type>RESPONSE</Type>
  <Seq>20140829084311000019</Seq>
  <Body>
    <Operation order="1" name="Get">
      <LampGroup>
        <SignalControlerID>33010058792223258</SignalControlerID>
        <LampGroupNo>1</LampGroupNo>
        <Direction>0</Direction>
        <Type>10</Type>
      </LampGroup>
    </Operation>
  </Body>
</Message>
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
    # cross_report_ctrl = CrossReportCtrl('CrossCycle')
    # cross_report_ctrl.get_cross_id_list()
    # cross_report_ctrl.set_response_data()
    #
    # print(cross_report_ctrl.response_date)
    #
    # xml_handler.xml_construct(cross_report_ctrl.response_date, cross_report_ctrl.data_type)
    #
    # print(xml_handler.response_data_xml)

    #
    sys_info = LampGroup('123')
    # sys_info.set_request_data()
    # xml_handler.xml_construct(sys_info.request_data, sys_info.data_type)
    # print(xml_handler.request_data_dict)
    sys_info.parse_response_data(xml_handler.request_data_dict)



    # 系统参数返回
    # print(xml_handler.response_data_xml)

