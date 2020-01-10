import xmltodict


class XmlHandler(object):
    def __init__(self):
        self.token = ''
        self.client_address = ''
        self.seq = ''
        self.operation_order = ''
        self.operation_name = ''
        self.data_type = ''
        self.data_dict = {}

    def xml_parse(self, xml_data):
        data = xmltodict.parse(xml_data)

        data = data.get('Message', {})

        self.token = data.get('Token', '')
        self.client_address = data.get('From', '')
        self.seq = data.get('Seq')

        data = data.get('Body', {})
        data = data.get('Operation', {})
        self.operation_order = data.get('@order', '')
        self.operation_name = data.get('@name', '')
        self.data_type = tuple(data.keys())[-1]

        self.data_dict = data.get(self.data_type, {})

        for k, v in self.data_dict.items():
            print(k, v)









