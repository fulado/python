"""
处理xml数据
"""
import hashlib
import time


from utils.xml_tools import generate_ordered_dict


# 数据基类
class XmlData(object):
    def __init__(self, request_data):
        self.request_data = request_data
        self.response_date = {}
        self.token = ''
        self.data_type = 'RESPONSE'


# 登录数据
class LoginData(XmlData):
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
        # 判断账号密码
        if self.username == 'fengxian' and self.password == 'signal':
            login_success = True
        else:
            login_success = False

        if login_success:
            # 如果账号密码正确，构造登录成功数据
            self.generate_token()
            self.username = 'fengxian'
            self.password = 'signal'

            # 生产token
            self.generate_token()

            # 构造返回数据
            object_list = [('UserName', self.username),
                           ('Pwd', self.password),
                           ]

            operation_list = [('SDO_User', object_list),
                              ]
        else:
            # 如果账号密码错误，构造登录失败数据
            object_list = [('ErrObj', 'SDO_User'),
                           ('ErrType', 'SDE_UserName'),
                           ('ErrDesc', '用户名错误'),
                           ]

            operation_list = [('SDO_User', object_list),
                              ]

            self.data_type = 'ERROR'

        operation_order = '1'
        operation_name = 'Login'

        self.response_date = generate_ordered_dict(operation_order, operation_name, operation_list)


# 心跳
class HearBeat(XmlData):
    def __init__(self, request_data):
        super(HearBeat, self).__init__(request_data)
        self.data_type = 'PUSH'

    def set_response_data(self):
        operation_list = [('SDO_HeartBeat', [])]
        operation_order = '7'
        operation_name = 'notify'

        self.response_date = generate_ordered_dict(operation_order, operation_name, operation_list)
















































