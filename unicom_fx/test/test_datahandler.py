from server_2.data_handler import DataHandler
from static_data.static_data_subscribe import StaticDataSubscribe

def main():
    lamp_group_data = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>1E1969411E51CA7D9A0AEC64D8E90A2525B979C3</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313144608000001</Seq><Body><Operation name="Notify" order="1"><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>1</LampGroupNo><Direction>0</Direction><Type>10</Type><PhaseNo>5</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>2</LampGroupNo><Direction>0</Direction><Type>10</Type><PhaseNo>3</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>3</LampGroupNo><Direction>0</Direction><Type>31</Type><PhaseNo>3</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>4</LampGroupNo><Direction>2</Direction><Type>10</Type><PhaseNo>2</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>5</LampGroupNo><Direction>2</Direction><Type>10</Type><PhaseNo>1</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>6</LampGroupNo><Direction>2</Direction><Type>31</Type><PhaseNo>1</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>7</LampGroupNo><Direction>4</Direction><Type>10</Type><PhaseNo>4,5</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>8</LampGroupNo><Direction>4</Direction><Type>10</Type><PhaseNo>4,3</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>9</LampGroupNo><Direction>4</Direction><Type>31</Type><PhaseNo>3,4</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>10</LampGroupNo><Direction>4</Direction><Type>21</Type><PhaseNo>5</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>11</LampGroupNo><Direction>6</Direction><Type>10</Type><PhaseNo>2</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>12</LampGroupNo><Direction>6</Direction><Type>10</Type><PhaseNo>1</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>13</LampGroupNo><Direction>6</Direction><Type>31</Type><PhaseNo>1</PhaseNo></LampGroup></Operation></Body></Message>
    """

    lane_param_data = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>1E1969411E51CA7D9A0AEC64D8E90A2525B979C3</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313144608000001</Seq><Body><Operation name="Notify" order="1"><LaneParam><CrossID>31012000000045</CrossID><LaneNo>8</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>7</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>6</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>5</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>31</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>16</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>15</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>14</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>13</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>22</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>22</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>21</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>20</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>31</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>30</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>29</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>28</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>27</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>1</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>2</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>3</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>4</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>9</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>10</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>11</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>12</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>17</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>18</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>19</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>23</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>24</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>25</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000045</CrossID><LaneNo>26</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam></Operation></Body></Message>"""

    dh = DataHandler('send data queue')

    # dh.xml_parse(lane_param_data)
    # print(dh.object_type)
    # print(dh.recv_data_dict)

    dh.data_subscribe_handle()

    # dh.get_signal_id_list()
    # print(dh.signal_id_list)
    # print(len(dh.signal_id_list))

    # dh.data_handle()

    # data = data_handler.recv_data_dict.get('StageNoList').keys()
    # print(list(data))
    # for k, v in data_handler.recv_data_dict.items():
    #     print(k, v)

    # dh.get_cross_id_list()
    # # print(dh.cross_id_list)
    #
    # dh.get_signal_id_list()
    # # print(dh.signal_id_list)
    #
    # for cross_id in dh.cross_id_list:
    #
    #     static_data_subscribe = StaticDataSubscribe('abc', cross_id, 'LampGroup')
    #     static_data_subscribe.create_send_data()
    #
    #     print(static_data_subscribe.send_data_xml)


if __name__ == '__main__':
    main()
















