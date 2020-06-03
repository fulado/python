# encoding:utf-8

from server_2.data_handler import DataHandler
from static_data.static_data import StaticData


recv_data_xml = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>D27967B2B6EF6611F8A23F846592D7A5CA861260</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200317103339000897</Seq><Body><Operation name="Get" order="5"><PlanParam><CrossID>31012000000034</CrossID><PlanNo>1</PlanNo><CycleLen>144</CycleLen><CoordPhaseNo>0</CoordPhaseNo><OffSet>0</OffSet><StageNoList><StageNo>1</StageNo><StageNo>2</StageNo><StageNo>3</StageNo><StageNo>4</StageNo></StageNoList></PlanParam><PlanParam><CrossID>31012000000034</CrossID><PlanNo>2</PlanNo><CycleLen>172</CycleLen><CoordPhaseNo>0</CoordPhaseNo><OffSet>0</OffSet><StageNoList><StageNo>5</StageNo><StageNo>6</StageNo><StageNo>7</StageNo><StageNo>8</StageNo></StageNoList></PlanParam><PlanParam><CrossID>31012000000034</CrossID><PlanNo>3</PlanNo><CycleLen>162</CycleLen><CoordPhaseNo>0</CoordPhaseNo><OffSet>0</OffSet><StageNoList><StageNo>9</StageNo><StageNo>10</StageNo><StageNo>11</StageNo><StageNo>12</StageNo></StageNoList></PlanParam><PlanParam><CrossID>31012000000034</CrossID><PlanNo>4</PlanNo><CycleLen>153</CycleLen><CoordPhaseNo>0</CoordPhaseNo><OffSet>0</OffSet><StageNoList><StageNo>13</StageNo><StageNo>14</StageNo><StageNo>15</StageNo><StageNo>16</StageNo></StageNoList></PlanParam></Operation></Body></Message>
"""


data_handler = DataHandler('send data queue', 'put datahub queue')
data_handler.xml_parse(recv_data_xml)

# print(data_handler.data_type)
# print(data_handler.object_type)
# print(data_handler.recv_data_dict)
#
# print(data_handler.recv_data_dict.get('SignalControlerID'))
# print(data_handler.recv_data_dict.get('CrossIDList'))

static_data = StaticData('PlanParam')
static_data.parse_recv_data(data_handler.recv_data_dict)
static_data.save_data_to_file()
static_data.convert_data_for_datahub()

print(static_data.obj_name)
print(static_data.recv_data)
# print(static_data.recv_data[0])
# print(static_data.recv_data[1])

# print(static_data.recv_data[0].get('SignalControlerID'))
# print(static_data.recv_data.get('CrossIDList').get('CrossID'))
print(static_data.datahub_put_data)














