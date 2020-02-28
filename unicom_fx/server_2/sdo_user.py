"""
登录
"""
import hashlib
import time

from .utils import generate_ordered_dict, xml_construct


class SdoUser(object):
    def __init__(self, send_data_queue, seq, data_dict):
        self.send_data_queue = send_data_queue
        self.seq = seq
        self.data_dict = data_dict
        self.username = ''
        self.password = ''
        self.token = ''
        self.data_type = ''
        self.send_data_xml = ''

    # 获取登录信息
    def get_user_info(self):
        self.username = self.data_dict.get('UserName', '')
        self.password = self.data_dict.get('Pwd', '')

    # 生成token
    def generate_token(self):
        self.token = hashlib.sha1(
            ('%s%s%d' % (self.username, self.password, int(time.time()))).encode()).hexdigest().upper()

    # 生成登录数据
    def create_login_response_data(self):
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

            self.data_type = 'RESPONSE'
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

        send_data_dict = generate_ordered_dict(operation_order, operation_name, operation_list)
        self.send_data_xml = xml_construct(send_data_dict, self.seq, self.token, self.data_type)

    # 将数据存入发送数据队列
    def put_send_data_into_queue(self):
        self.send_data_queue.put(self.send_data_xml)






















