"""
命令下发返回数据
"""
import time


class CmdResult(object):
    def __init__(self, obj_name):
        self.recv_data = {}
        self.obj_name = obj_name
        self.cross_id = None
        self.end_time = None
        self.coord_stage_no = None
        self.offset = None
        self.gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.return_info = None
        self.success = 1
        self.datahub_put_data = []

    # 解析返回结果数据
    def parse_recv_data(self, recv_data_dict):
        self.cross_id = recv_data_dict.get('CrossID')
        self.end_time = recv_data_dict.get('EndTime')
        self.coord_stage_no = recv_data_dict.get('CoordStageNo')
        self.offset = recv_data_dict.get('OffSet')

        split_time_list = []

        for split_time in recv_data_dict.get('SplitTimeList').get('SplitTime'):
            split_time_list.append({'stageNo': split_time.get('StageNo'),
                                    'Green': split_time.get('Green')})

        self.return_info = {'CrossID': self.cross_id,
                            'EndTime': self.end_time,
                            'CoordStageNo': self.coord_stage_no,
                            'OffSet': self.offset,
                            'SplitTimeList': split_time_list,
                            }

        self.return_info = str(self.return_info)  # 字典转换为json字符串

    # 构造datahub写入数据
    def convert_data_for_datahub(self):
        data_list = [self.cross_id,
                     self.end_time,
                     self.success,
                     self.gmt_create,
                     time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                     self.return_info
                     ]

        self.datahub_put_data = [self.obj_name, data_list]























