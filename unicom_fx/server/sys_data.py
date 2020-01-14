"""
处理xml数据
"""
import hashlib
import time
from collections import OrderedDict


from utils.xml_tools import generate_ordered_dict


# 数据基类
class SysData(object):
    def __init__(self, request_data):
        self.request_data = request_data
        self.response_data = {}
        self.token = ''
        self.data_type = 'RESPONSE'

    def set_response_data(self):
        pass


# 登录数据
class LoginData(SysData):
    def __init__(self, request_data):
        super(LoginData, self).__init__(request_data)
        self.username = ''
        self.password = ''

    # 获取登录信息
    def get_user_info(self):
        self.username = self.request_data.get('UserName', '')
        self.password = self.request_data.get('Pwd', '')

    # 生成token
    def generate_token(self):
        self.token = hashlib.sha1(('%s%s%d' % (self.username, self.password, int(time.time()))).encode()).hexdigest()

    # 生成登录数据
    def set_response_data(self):
        self.get_user_info()

        # 判断账号密码
        if self.username == 'fengxian' and self.password == 'fengxian':
            login_success = True
        else:
            login_success = False

        if login_success:
            # 如果账号密码正确，构造登录成功数据
            self.generate_token()
            self.username = 'fengxian'
            self.password = 'fengxian'

            # 生产token
            self.generate_token()

            # 构造返回数据
            object_list = [('UserName', self.username),
                           ('Pwd', self.password),
                           ]

            operation_list = [('SDO_User', object_list),
                              ]

            print('%s : 登陆成功' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        else:
            # 如果账号密码错误，构造登录失败数据
            object_list = [('ErrObj', 'SDO_User'),
                           ('ErrType', 'SDE_UserName'),
                           ('ErrDesc', '用户名错误'),
                           ]

            operation_list = [('SDO_User', object_list),
                              ]

            self.data_type = 'ERROR'

            print('%s : 登陆失败' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        operation_order = '1'
        operation_name = 'Login'

        self.response_data = generate_ordered_dict(operation_order, operation_name, operation_list)


# 心跳
class HearBeat(object):
    def __init__(self):
        self.data_type = 'PUSH'
        self.response_data = ''

    def set_response_data(self):
        operation_list = [('SDO_HeartBeat', [])]
        operation_order = '7'
        operation_name = 'notify'

        self.response_data = generate_ordered_dict(operation_order, operation_name, operation_list)


# 订阅
class CrossReportCtrl(object):
    def __init__(self, data_name):
        self.data_type = 'REQUEST'
        self.object_type = 'CrossReportCtrl'
        self.data_name = data_name
        self.cross_id_list = []
        self.response_data = ''

    # 获取路口id列表
    def get_cross_id_list(self):
        self.cross_id_list = ['452',
                              '411',
                              '2629']

    # 创建订阅数据
    # def set_response_data(self):
    #     cross_id_list = [('CrossID', self.cross_id_list),
    #                      ]
    #
    #     object_list = [('Cmd', 'Start'),
    #                    ('Type', self.data_name),
    #                    ('CrossIDList', cross_id_list),
    #                    ]
    #
    #     operation_list = [(self.object_type, object_list),
    #                       ]
    #
    #     operation_order = '1'
    #     operation_name = 'Set'
    #     print(operation_list)
    #     self.response_data = generate_ordered_dict(operation_order, operation_name, operation_list)
    def set_response_data(self):
        cross_id_list_element = OrderedDict()
        cross_id_list_element['CrossID'] = self.cross_id_list

        cross_report_ctrl_element = OrderedDict()
        cross_report_ctrl_element['Cmd'] = 'Start'
        cross_report_ctrl_element['Type'] = self.data_name
        cross_report_ctrl_element['CrossIDList'] = cross_id_list_element

        operation_element = OrderedDict()
        operation_element['@order '] = '1'
        operation_element['@name '] = 'Set'
        operation_element['Operation '] = cross_report_ctrl_element

        self.response_data = operation_element








































