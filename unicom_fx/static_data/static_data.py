"""
静态数据
"""
import time


class StaticData(object):
    def __init__(self, obj_name):
        self.recv_data = {}
        self.obj_name = obj_name
        self.file_name = '../data/error.txt'
        self.datahub_put_data = []

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):

        if self.obj_name == 'SysInfo':
            # 系统参数/区域参数
            self.recv_data = recv_data_dict.get('SignalControlerIDList', {}).get('SignalControlerID', [])
            self.file_name = '../data/signal_list.txt'

        elif self.obj_name == 'RegionParam':
            # 区域参数
            self.recv_data = recv_data_dict.get('CrossIDList', {}).get('CrossID', [])
            self.file_name = '../data/cross_list.txt'

        elif self.obj_name == 'LampGroup':
            # 灯组参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/lamp_group/%s.txt' % recv_data_dict[0].get('SignalControlerID')

        elif self.obj_name == 'LaneParam':
            # 车道参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/lane_param/%s.txt' % recv_data_dict[0].get('CrossID')

        elif self.obj_name == 'StageParam':
            # 相位参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/stage_param/%s.txt' % recv_data_dict.get('CrossID')

        elif self.obj_name == 'PlanParam':
            # 相位参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/plan_param/%s.txt' % recv_data_dict.get('CrossID')

        elif self.obj_name == 'SignalControler':
            # 信号机参数
            self.recv_data = recv_data_dict
            self.file_name = '../data/signal_controller/%s.txt' % recv_data_dict.get('SignalControlerID')

        else:
            pass

    # 转化数据为列表
    def convert_data_for_datahub(self):
        dt = time.strftime('%Y%m%d', time.localtime())
        adcode = '310000'

        # 信号机信息
        if self.obj_name == 'SignalControler':
            data_list = self.set_put_data_list_signal_controller(dt, adcode)

        # 灯组信息, 车道信息
        elif self.obj_name in ('LampGroup', 'LaneParam'):
            data_list = self.set_put_data_list_lamp_group_lane_param(dt, adcode)

        #
        # elif self.obj_name == :
        #     data_list = self.set_put_data_list_lamp_group_lane_param(dt, adcode)

        else:
            pass

        self.datahub_put_data = [self.obj_name, data_list]

    # 生成信号机信息datahub发布数据列表
    def set_put_data_list_signal_controller(self, dt, adcode):
        data_list_signal_controller = []

        signal_id = self.recv_data.get('SignalControlerID', '')
        cross_id_list = self.recv_data.get('CrossIDList', {}).get('CrossID', '')

        if isinstance(cross_id_list, list):
            cross_id_list = ','.join(cross_id_list)
        else:
            pass

        data_list_signal_controller.append(signal_id)
        data_list_signal_controller.append(cross_id_list)

        data_list_signal_controller.append(dt)
        data_list_signal_controller.append(adcode)

        return [data_list_signal_controller, ]

    # 生成灯组信息datahub发布数据列表
    def set_put_data_list_lamp_group_lane_param(self, dt, adcode):
        data_list_lamp_group = []

        for data_dict in self.recv_data:
            data_list_tmp = list()

            if self.obj_name == 'LampGroup':
                data_list_tmp.append(data_dict.get('SignalControlerID'))
                data_list_tmp.append(data_dict.get('LampGroupNo'))
                data_list_tmp.append(data_dict.get('Direction'))
                data_list_tmp.append(data_dict.get('Type'))
            else:
                data_list_tmp.append(data_dict.get('CrossID'))
                data_list_tmp.append(data_dict.get('LaneNo'))
                data_list_tmp.append(data_dict.get('Direction'))
                data_list_tmp.append(data_dict.get('Attribute'))
                data_list_tmp.append(data_dict.get('Movement'))
                data_list_tmp.append(data_dict.get('Movement'))

            data_list_tmp.append(dt)
            data_list_tmp.append(adcode)

            data_list_lamp_group.append(data_list_tmp)

        return data_list_lamp_group

    # 保存数据
    def save_data_to_file(self):
        file = open(self.file_name, 'w')
        # print(self.file_name)
        if self.obj_name == 'SysInfo' or self.obj_name == 'RegionParam':
            self.save_data_for_list(file)

        elif self.obj_name == 'LampGroup' or self.obj_name == 'LaneParam':
            self.save_data_for_list_dict(file)

        elif self.obj_name == 'StageParam':
            self.save_data_for_dict_list(file, 'PhaseNoList')

        elif self.obj_name == 'PlanParam':
            self.save_data_for_dict_list(file, 'StageNoList')

        elif self.obj_name == 'SignalControler':
            self.save_data_for_dict_list(file, 'CrossIDList')

        else:
            pass

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

    # 保存灯组, 车道数据, 数据是一个列表, 列表中的的值是字典格式
    def save_data_for_list_dict(self, file):
        try:
            for data_dict in self.recv_data:
                for k, v in data_dict.items():
                    file.write('%s: %s' % (k, v))
                    file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()












