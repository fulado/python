import xml.etree.ElementTree as xml_et


class XmlHandler(object):
    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.token = ''
        self.client_address = ''
        self.seq = ''
        self.operation_name = ''
        self.object_name = ''

    def xml_parse(self):
        root = xml_et.fromstring(self.xml_data)

        self.token = root.find('Token').text
        self.client_address = root.find('From').text
        self.seq = root.find('Seq').text












