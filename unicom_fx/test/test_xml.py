import xml.etree.ElementTree as xml_et
import xmltodict
from pprint import pprint
import json

from server.xml_handler import XmlHandler


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
    <?xml version="1.0" encoding="UTF-8"?> <Message> <Version>版本号</Version> <Token></Token> <From>源地址</From> <To><Address><Sys>TICP</Sys><SubSys/><Instance/></Address></To> <Type>REQUEST</Type> <Seq>序列号</Seq> <Body> <Operation order="1" name="Login"> <SDO_User> <UserName>用户名</UserName> <Pwd>口令</Pwd>
</SDO_User > </Operation> </Body> </Message>
    """

    # parse_xml(xml_data.strip())

    xml_handler = XmlHandler()
    xml_handler.xml_parse(xml_data.strip())


