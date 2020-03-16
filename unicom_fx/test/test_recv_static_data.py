from server_2.data_handler import DataHandler
from static_data.static_data import StaticData


recv_data_xml = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>D27967B2B6EF6611F8A23F846592D7A5CA861260</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200316160904000835</Seq><Body><Operation name="Get" order="5"><LaneParam><CrossID>31012000000010</CrossID><LaneNo>6</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>5</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>4</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>15</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>14</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>13</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>12</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>11</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>7</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>21</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>22</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>20</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>19</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>28</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>27</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>26</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>25</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>1</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>2</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>3</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>8</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>9</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>10</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>16</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>17</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>18</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>22</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>23</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>24</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam></Operation></Body></Message>"""

data_handler = DataHandler('send data queue', 'put datahub queue')
data_handler.xml_parse(recv_data_xml)

# print(data_handler.data_type)
# print(data_handler.object_type)
# print(data_handler.recv_data_dict)
#
# print(data_handler.recv_data_dict.get('SignalControlerID'))
# print(data_handler.recv_data_dict.get('CrossIDList'))

static_data = StaticData('LaneParam')
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












