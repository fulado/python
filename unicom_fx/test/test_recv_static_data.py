# encoding:utf-8

from server_2.data_handler import DataHandler
from static_data.static_data import StaticData
from command.cmd_result import CmdResult


recv_data_xml = """<?xml version="1.0" encoding="utf-8"?>
<Message><Version>1.0</Version><Token>6B11E4FE5869ED479AD887C80CB9C2D3FB8B5977</Token><From><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>REQUEST</Type><Seq>20200512141114000699</Seq><Body><Operation order="6" name="Set"><TempPlanParam><CrossID>31012000000051</CrossID><CoordStageNo>0</CoordStageNo><OffSet>0</OffSet><EndTime>2020-05-12 23:59:59</EndTime><SplitTimeList><SplitTime><StageNo>3</StageNo><Green>61</Green></SplitTime><SplitTime><StageNo>4</StageNo><Green>25</Green></SplitTime></SplitTimeList></TempPlanParam></Operation></Body></Message>"""

data_handler = DataHandler('123456', 'send data queue', 'put datahub queue')
data_handler.xml_parse(recv_data_xml)

# print(data_handler.data_type)
# print(data_handler.object_type)
print(data_handler.recv_data_dict)

cmd_result = CmdResult('RESPONSE')
cmd_result.parse_recv_data(data_handler.recv_data_dict)
cmd_result.convert_data_for_datahub()
print(cmd_result.datahub_put_data)

# print(data_handler.recv_data_dict.get('CrossID'))
# print(data_handler.recv_data_dict.get('CoordStageNo'))
# print(data_handler.recv_data_dict.get('OffSet'))
# print(data_handler.recv_data_dict.get('EndTime'))
# print(data_handler.recv_data_dict.get('SplitTimeList').get('SplitTime'))

# print(data_handler.recv_data_dict.get('SignalControlerID'))
# print(data_handler.recv_data_dict.get('CrossIDList'))

# static_data = StaticData('PlanParam')
# static_data.parse_recv_data(data_handler.recv_data_dict)
# static_data.save_data_to_file()
# static_data.convert_data_for_datahub()

# print(static_data.obj_name)
# print(static_data.recv_data)
# print(static_data.recv_data[0])
# print(static_data.recv_data[1])

# print(static_data.recv_data[0].get('SignalControlerID'))
# print(static_data.recv_data.get('CrossIDList').get('CrossID'))
# print(static_data.datahub_put_data)














