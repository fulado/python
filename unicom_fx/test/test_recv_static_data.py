# encoding:utf-8

from server_2.data_handler import DataHandler
from static_data.static_data import StaticData


recv_data_xml = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>1E1969411E51CA7D9A0AEC64D8E90A2525B979C3</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313144608000001</Seq><Body><Operation name="Notify" order="1"><PhaseParam><CrossID>31012000000050</CrossID><PhaseNo>1</PhaseNo><PhaseName>相位1</PhaseName><Feature>1</Feature><Attribute>1</Attribute><LaneNoList><LaneNo>6</LaneNo><LaneNo>5</LaneNo><LaneNo>20</LaneNo><LaneNo>19</LaneNo></LaneNoList><PedDirList><Direction>0-1-1</Direction><Direction>4-1-1</Direction></PedDirList></PhaseParam><PhaseParam><CrossID>31012000000050</CrossID><PhaseNo>2</PhaseNo><PhaseName>相位2</PhaseName><Feature>1</Feature><Attribute>1</Attribute><LaneNoList><LaneNo>20</LaneNo><LaneNo>19</LaneNo><LaneNo>18</LaneNo></LaneNoList><PedDirList></PedDirList></PhaseParam><PhaseParam><CrossID>31012000000050</CrossID><PhaseNo>3</PhaseNo><PhaseName>相位3</PhaseName><Feature>1</Feature><Attribute>1</Attribute><LaneNoList><LaneNo>4</LaneNo><LaneNo>21</LaneNo><LaneNo>18</LaneNo></LaneNoList><PedDirList></PedDirList></PhaseParam><PhaseParam><CrossID>31012000000050</CrossID><PhaseNo>4</PhaseNo><PhaseName>相位4</PhaseName><Feature>1</Feature><Attribute>1</Attribute><LaneNoList><LaneNo>13</LaneNo><LaneNo>12</LaneNo><LaneNo>28</LaneNo><LaneNo>27</LaneNo></LaneNoList><PedDirList><Direction>2-1-1</Direction><Direction>6-1-1</Direction></PedDirList></PhaseParam><PhaseParam><CrossID>31012000000050</CrossID><PhaseNo>5</PhaseNo><PhaseName>相位5</PhaseName><Feature>1</Feature><Attribute>1</Attribute><LaneNoList><LaneNo>11</LaneNo><LaneNo>26</LaneNo></LaneNoList><PedDirList></PedDirList></PhaseParam></Operation></Body></Message>"""


data_handler = DataHandler('send data queue', 'put datahub queue')
data_handler.xml_parse(recv_data_xml)

# print(data_handler.data_type)
# print(data_handler.object_type)
# print(data_handler.recv_data_dict)
#
# print(data_handler.recv_data_dict.get('SignalControlerID'))
# print(data_handler.recv_data_dict.get('CrossIDList'))

static_data = StaticData('PhaseParam')
static_data.parse_recv_data(data_handler.recv_data_dict)
static_data.save_data_to_file()
static_data.convert_data_for_datahub()

print(static_data.obj_name)
print(static_data.recv_data)
print(static_data.recv_data[0])
print(static_data.recv_data[1])

# print(static_data.recv_data[0].get('SignalControlerID'))
# print(static_data.recv_data.get('CrossIDList').get('CrossID'))
print(static_data.datahub_put_data)














