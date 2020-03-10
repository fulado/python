"""
静态数据
"""


class StaticData(object):
    def __init__(self, obj_name):
        self.recv_data = {}
        self.obj_name = obj_name
        self.file_name = '../data/error.txt'

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):

        if self.obj_name == 'SysInfo':
            # 系统参数/区域参数
            self.recv_data = recv_data_dict.get('CrossIDList', {}).get('CrossID', [])
            self.file_name = '../data/signal_list.txt'

        elif self.obj_name == 'RegionParam':
            # 区域参数
            self.recv_data = recv_data_dict.get('CrossIDList', {}).get('CrossID', [])
            self.file_name = '../data/cross_list.txt'

        elif self.obj_name == 'LampParam':
            # 灯组参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/lamp_group/%s.txt' % recv_data_dict.get('SignalControlerID')

        elif self.obj_name == 'LaneParam':
            # 车道参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/lane_param/%s.txt' % recv_data_dict.get('CrossID')

        elif self.obj_name == 'StageParam':
            # 相位参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/stage_param/%s.txt' % recv_data_dict.get('CrossID')

        elif self.obj_name == 'PlanParam':
            # 相位参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/plan_param/%s.txt' % recv_data_dict.get('CrossID')

    # 保存数据
    def save_data_to_file(self):
        file = open(self.file_name, 'w')

        if self.obj_name == 'SysInfo' or self.obj_name == 'RegionParam':
            self.save_data_for_list(file)

        elif self.obj_name == 'LampParam' or self.obj_name == 'LampParam':
            self.save_data_for_dict(file)

        elif self.obj_name == 'StageParam':
            self.save_data_for_dict_list(file, 'PhaseNoList')

        elif self.obj_name == 'PlanParam':
            self.save_data_for_dict_list(file, 'StageNoList')

    # 保存系统, 区域等数据, 数据是一个列表
    def save_data_for_list(self, file):
        try:
            for data in self.recv_data:
                file.write(data)
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    # 保存灯组, 车道等数据, 数据是一个字典
    def save_data_for_dict(self, file):
        try:
            for k, v in self.recv_data.items():
                file.write('%s: %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    # 保存相位数据, 数据是一个字典, 并且字典的值中包含列表
    def save_data_for_dict_list(self, file, key_of_list):
        try:
            for k, v in self.recv_data.items():
                if k == key_of_list:
                    v = self.recv_data.get(key_of_list)
                    key_tmp = list(v.keys())[0]
                    v = v.get(key_tmp)
                else:
                    pass

                file.write('%s: %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()














