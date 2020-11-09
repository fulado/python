# encoding:utf-8

from server.data_handler import DataHandler
from static_data.static_data import StaticData
from command.cmd_result import CmdResult


recv_data_xml = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>02FCB106FB8742B0901E14BAFB0DD4B0411D5B82</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200615165558000987</Seq><Body><Operation name="Set" order="6"><TempPlanParam><CrossID>31012000000042</CrossID><CoordStageNo>7</CoordStageNo><OffSet>3</OffSet><EndTime>2020-06-15 18:00:00</EndTime><SplitTimeList><SplitTime><StageNo>7</StageNo><Green>36</Green></SplitTime><SplitTime><StageNo>8</StageNo><Green>79</Green></SplitTime><SplitTime><StageNo>9</StageNo><Green>37</Green></SplitTime></SplitTimeList></TempPlanParam></Operation></Body></Message>"""

data_handler = DataHandler('123456', 'send data queue', 'put datahub queue')
data_handler.xml_parse(recv_data_xml.strip())

data_handler.data_handle()
# print(data_handler.data_type)
# print(data_handler.object_type)
# print(data_handler.recv_data_dict)
# print(data_handler.is_error)
# print(data_handler.error_data)

# cmd_result = CmdResult(data_handler.object_type, data_handler.is_error)
# cmd_result.parse_recv_data(data_handler.recv_data_dict)
# cmd_result.convert_data_for_datahub()
# print(cmd_result.datahub_put_data)

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














