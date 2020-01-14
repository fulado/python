import xmltodict
import collections


class XmlHandler(object):
    def __init__(self):
        self.token = ''
        # 序列号（Seq）用于标识一对请求和应答类型数据包（REQUEST/RESPONSE）。Seq 取值唯一， 最大长度 20 位，
        # 采用 14 位日期（YYYYMMDDHHMMSS）+6 位顺序号（不足 6 位前补 0）；
        self.seq = ''
        self.client_address = 'UTCS'
        self.server_address = 'TICP'
        self.operation_order = ''
        self.operation_name = ''
        self.data_type = ''     # 数据包类型
        self.object_type = ''   # 数据对象类型，用于判断获得是何种数据
        self.request_data_dict = {}
        self.response_data_xml = ''

    # 解析请求xml
    def xml_parse(self, xml_data):
        data = xmltodict.parse(xml_data.strip())
        data = data.get('Message', {})

        # self.token = data.get('Token', '')
        # self.client_address = data.get('From', '')
        self.seq = data.get('Seq')

        data = data.get('Body', {})
        data = data.get('Operation', {})

        # self.operation_order = data.get('@order', '')
        # self.operation_name = data.get('@name', '')

        self.object_type = tuple(data.keys())[-1]
        self.request_data_dict = data.get(self.object_type, {})

    # 构造返回xml
    def xml_construct(self, dict_data, data_type='RESPONSE', token='', seq=''):
        self.token = token
        self.data_type = data_type
        self.seq = seq if seq != '' else self.seq

        message = collections.OrderedDict()
        message['Version'] = '1.0'
        message['Token'] = self.token

        # 构造From标签中的内容
        from_address = collections.OrderedDict()
        from_address['Sys'] = self.server_address
        from_address['SubSys'] = ''
        from_address['Instance'] = ''

        from_element = collections.OrderedDict()
        from_element['Address'] = from_address
        message['From'] = from_element

        # 构造To标签中的内容
        to_address = collections.OrderedDict()
        to_address['Sys'] = self.client_address
        to_address['SubSys'] = ''
        to_address['Instance'] = ''

        to_element = collections.OrderedDict()
        to_element['Address'] = to_address
        message['To'] = to_element

        message['Type'] = self.data_type
        message['Seq'] = self.seq
        message['Body'] = dict_data

        response_data_dict = collections.OrderedDict()
        response_data_dict['Message'] = message

        self.response_data_xml = xmltodict.unparse(response_data_dict)










