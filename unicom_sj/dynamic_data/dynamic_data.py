"""
信号机实时数据
"""
import time


# 数据基类
class DynamicData(object):
    def __init__(self, obj_name):
        self.recv_data = {}
        self.obj_name = obj_name
        self.file_name = '../data/error.txt'
        self.datahub_put_data = []

    # 获取保存文件路径
    def parse_recv_data(self, recv_data_dict):
        self.recv_data = recv_data_dict

        cross_id = recv_data_dict.get('CrossID', 'error')

        if cross_id != 'error':

            if self.obj_name == 'CrossCycle':
                self.file_name = '../data/%s/%s.txt' % ('cycle_rt', cross_id)
            elif self.obj_name == 'CrossStage':
                self.file_name = '../data/%s/%s.txt' % ('stage_rt', cross_id)
            else:
                pass

        else:
            pass

    # 保存数据
    def save_data_to_file(self):
        file = open(self.file_name, 'w')

        try:
            for k, v in self.recv_data.items():
                file.write('%s: %s' % (k, v))
                file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    # 转化数据为列表
    def convert_data_for_datahub(self):
        data_list_tmp = []
        for k, v in self.recv_data.items():
            # 如果是数值类型的字段, 需要转化为整型
            if k in ('LastStageLen', 'CurStageLen', 'CurStageRemainLen', 'LastCycleLen', 'CurCycleLen',
                     'CurCycleRemainLen'):
                try:
                    data_list_tmp.append(int(float(v)))
                except ValueError:
                    data_list_tmp.append(0)
            else:
                data_list_tmp.append(v)

        dt = time.strftime('%Y%m%d', time.localtime())
        adcode = '310000'

        data_list_tmp.append(dt)
        data_list_tmp.append(adcode)

        self.datahub_put_data = [self.obj_name, [data_list_tmp, ]]

    # 转化流量数据为列表
    def convert_traffic_data_for_datahub(self):
        cross_id = self.recv_data.get('CrossID')
        end_time = self.recv_data.get('EndTime')
        interval = int(float(self.recv_data.get('Interval')))
        traffic_data_list = self.recv_data.get('DataList').get('Data')

        data_list_tmp = []
        for traffic_data in traffic_data_list:

            lane_data = [cross_id, end_time, interval]

            for k, v in traffic_data.items():
                if k == 'LaneNo':
                    lane_data.append(v)
                else:
                    lane_data.append(int(float(v)))

            lane_data.append(time.strftime('%Y%m%d', time.localtime()))
            lane_data.append('310000')

            data_list_tmp.append(lane_data)

        self.datahub_put_data = [self.obj_name, data_list_tmp]


# # 路口周期
# class CrossCycle(DynamicData):
#     def get_file_name(self):
#         cross_id = self.recv_data_dict.get('CrossID', 'error')
#
#         self.file_name = '../data/cycle_rt/%s.txt' % cross_id
#
#
# # 路口阶段
# class CrossStage(DynamicData):
#     def get_file_name(self):
#         cross_id = self.recv_data_dict.get('CrossID', 'error')
#
#         self.file_name = '../data/stage_rt/%s.txt' % cross_id































