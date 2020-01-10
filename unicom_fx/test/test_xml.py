import xml.etree.ElementTree as xml_et


def parse_xml(xml_data):
    root = xml_et.fromstring(xml_data)

    # version = root.find('Version').text
    # token = root.find('Token').text
    # client_address = root.find('From').text
    # data_type = root.find('Type').text
    # seq = root.find('Seq').text
    #
    # body = root.find('Body')
    #
    # operation = body.find('Operation')
    # operation_name = operation.attrib.get('name', '')
    #
    # print(operation_name)
    #
    # obj = operation[0]
    #
    # print(obj.tag)
    #
    # username = obj.find('UserName').text
    # print(username)
    #
    # password = obj.find('Pwd').text
    # print(password)

    for child in root:
        print(child.tag, child.attrib, child.text)


def get_child_element(element):

    for child in element:
        get_child_element(child)
        


if __name__ == '__main__':
    xml_data = """
    <?xml version="1.0" encoding="UTF-8"?> <Message> <Version>版本号</Version> <Token></Token> <From>源地址</From> <To><Address><Sys>TICP</Sys><SubSys/><Instance/></Address></To> <Type>REQUEST</Type> <Seq>序列号</Seq> <Body> <Operation order="1" name="Login"> <SDO_User> <UserName>用户名</UserName> <Pwd>口令</Pwd>
</SDO_User > </Operation> </Body> </Message>
    """

    parse_xml(xml_data.strip())


