from server_2.data_handler import DataHandler
from static_data.static_data_subscribe import StaticDataSubscribe

def main():
    lamp_group_data = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>1E1969411E51CA7D9A0AEC64D8E90A2525B979C3</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313144608000001</Seq><Body><Operation name="Notify" order="1"><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>1</LampGroupNo><Direction>0</Direction><Type>10</Type><PhaseNo>5</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>2</LampGroupNo><Direction>0</Direction><Type>10</Type><PhaseNo>3</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>3</LampGroupNo><Direction>0</Direction><Type>31</Type><PhaseNo>3</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>4</LampGroupNo><Direction>2</Direction><Type>10</Type><PhaseNo>2</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>5</LampGroupNo><Direction>2</Direction><Type>10</Type><PhaseNo>1</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>6</LampGroupNo><Direction>2</Direction><Type>31</Type><PhaseNo>1</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>7</LampGroupNo><Direction>4</Direction><Type>10</Type><PhaseNo>4,5</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>8</LampGroupNo><Direction>4</Direction><Type>10</Type><PhaseNo>4,3</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>9</LampGroupNo><Direction>4</Direction><Type>31</Type><PhaseNo>3,4</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>10</LampGroupNo><Direction>4</Direction><Type>21</Type><PhaseNo>5</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>11</LampGroupNo><Direction>6</Direction><Type>10</Type><PhaseNo>2</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>12</LampGroupNo><Direction>6</Direction><Type>10</Type><PhaseNo>1</PhaseNo></LampGroup><LampGroup><SignalControlerID>31012000000000006</SignalControlerID><LampGroupNo>13</LampGroupNo><Direction>6</Direction><Type>31</Type><PhaseNo>1</PhaseNo></LampGroup></Operation></Body></Message>
    """

    # lane_param_data = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>C080D4B8264C6BA41899F93430853C2A32D246F7</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313174830000001</Seq><Body><Operation name="Notify" order="1"><CrossCycle><CrossID>31012000000010</CrossID><StartTime>2020-03-13 17:47:40</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000013</CrossID><StartTime>2020-03-13 17:45:26</StartTime><LastCycleLen>80.0</LastCycleLen><CurCycleLen>80.0</CurCycleLen><CurCycleRemainLen>80.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000064</CrossID><StartTime>2020-03-13 17:45:37</StartTime><LastCycleLen>168.0</LastCycleLen><CurCycleLen>168.0</CurCycleLen><CurCycleRemainLen>168.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000004</CrossID><StartTime>2020-03-13 17:45:14</StartTime><LastCycleLen>132.0</LastCycleLen><CurCycleLen>132.0</CurCycleLen><CurCycleRemainLen>132.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000063</CrossID><StartTime>2020-03-13 17:45:42</StartTime><LastCycleLen>152.0</LastCycleLen><CurCycleLen>152.0</CurCycleLen><CurCycleRemainLen>152.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000008</CrossID><StartTime>2020-03-13 17:46:29</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000024</CrossID><StartTime>2020-03-13 17:44:52</StartTime><LastCycleLen>167.0</LastCycleLen><CurCycleLen>167.0</CurCycleLen><CurCycleRemainLen>167.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000046</CrossID><StartTime>2020-03-13 17:45:47</StartTime><LastCycleLen>120.0</LastCycleLen><CurCycleLen>120.0</CurCycleLen><CurCycleRemainLen>120.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000005</CrossID><StartTime>2020-03-13 17:44:25</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000069</CrossID><StartTime>2020-03-13 17:46:31</StartTime><LastCycleLen>93.0</LastCycleLen><CurCycleLen>93.0</CurCycleLen><CurCycleRemainLen>93.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000027</CrossID><StartTime>2020-03-13 17:46:12</StartTime><LastCycleLen>167.0</LastCycleLen><CurCycleLen>167.0</CurCycleLen><CurCycleRemainLen>167.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000058</CrossID><StartTime>2020-03-13 17:45:26</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000018</CrossID><StartTime>2020-03-13 17:45:25</StartTime><LastCycleLen>142.0</LastCycleLen><CurCycleLen>142.0</CurCycleLen><CurCycleRemainLen>142.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000034</CrossID><StartTime>2020-03-13 17:45:16</StartTime><LastCycleLen>162.0</LastCycleLen><CurCycleLen>162.0</CurCycleLen><CurCycleRemainLen>162.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000006</CrossID><StartTime>2020-03-13 17:45:31</StartTime><LastCycleLen>86.0</LastCycleLen><CurCycleLen>86.0</CurCycleLen><CurCycleRemainLen>86.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000036</CrossID><StartTime>2020-03-13 17:45:48</StartTime><LastCycleLen>162.0</LastCycleLen><CurCycleLen>162.0</CurCycleLen><CurCycleRemainLen>162.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000057</CrossID><StartTime>2020-03-13 17:45:25</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000068</CrossID><StartTime>2020-03-13 17:46:33</StartTime><LastCycleLen>87.0</LastCycleLen><CurCycleLen>87.0</CurCycleLen><CurCycleRemainLen>87.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000020</CrossID><StartTime>2020-03-13 17:46:15</StartTime><LastCycleLen>99.0</LastCycleLen><CurCycleLen>99.0</CurCycleLen><CurCycleRemainLen>99.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000043</CrossID><StartTime>2020-03-13 17:44:51</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000042</CrossID><StartTime>1970-01-01 08:00:00</StartTime></CrossCycle><CrossCycle><CrossID>31012000000016</CrossID><StartTime>2020-03-13 17:45:26</StartTime><LastCycleLen>142.0</LastCycleLen><CurCycleLen>142.0</CurCycleLen><CurCycleRemainLen>142.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000060</CrossID><StartTime>2020-03-13 17:45:15</StartTime><LastCycleLen>164.0</LastCycleLen><CurCycleLen>164.0</CurCycleLen><CurCycleRemainLen>164.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000025</CrossID><StartTime>2020-03-13 17:46:25</StartTime><LastCycleLen>78.0</LastCycleLen><CurCycleLen>78.0</CurCycleLen><CurCycleRemainLen>78.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000037</CrossID><StartTime>2020-03-13 17:45:50</StartTime><LastCycleLen>162.0</LastCycleLen><CurCycleLen>162.0</CurCycleLen><CurCycleRemainLen>162.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000029</CrossID><StartTime>2020-03-13 17:45:17</StartTime><LastCycleLen>150.0</LastCycleLen><CurCycleLen>150.0</CurCycleLen><CurCycleRemainLen>150.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000040</CrossID><StartTime>2020-03-13 17:45:13</StartTime><LastCycleLen>153.0</LastCycleLen><CurCycleLen>153.0</CurCycleLen><CurCycleRemainLen>153.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000065</CrossID><StartTime>2020-03-13 17:45:22</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000048</CrossID><StartTime>2020-03-13 17:44:56</StartTime><LastCycleLen>152.0</LastCycleLen><CurCycleLen>152.0</CurCycleLen><CurCycleRemainLen>152.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000061</CrossID><StartTime>2020-03-13 17:44:03</StartTime><LastCycleLen>165.0</LastCycleLen><CurCycleLen>165.0</CurCycleLen><CurCycleRemainLen>165.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000021</CrossID><StartTime>2020-03-13 17:46:01</StartTime><LastCycleLen>84.0</LastCycleLen><CurCycleLen>84.0</CurCycleLen><CurCycleRemainLen>84.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000067</CrossID><StartTime>2020-03-13 17:46:08</StartTime><LastCycleLen>73.0</LastCycleLen><CurCycleLen>73.0</CurCycleLen><CurCycleRemainLen>73.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000038</CrossID><StartTime>2020-03-13 17:46:08</StartTime><LastCycleLen>104.0</LastCycleLen><CurCycleLen>104.0</CurCycleLen><CurCycleRemainLen>104.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000015</CrossID><StartTime>2020-03-13 17:45:50</StartTime><LastCycleLen>169.0</LastCycleLen><CurCycleLen>169.0</CurCycleLen><CurCycleRemainLen>169.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000062</CrossID><StartTime>2020-03-13 17:44:34</StartTime><LastCycleLen>152.0</LastCycleLen><CurCycleLen>152.0</CurCycleLen><CurCycleRemainLen>152.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000053</CrossID><StartTime>2020-03-13 17:46:42</StartTime><LastCycleLen>148.0</LastCycleLen><CurCycleLen>148.0</CurCycleLen><CurCycleRemainLen>148.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000041</CrossID><StartTime>2020-03-13 17:44:49</StartTime><LastCycleLen>153.0</LastCycleLen><CurCycleLen>153.0</CurCycleLen><CurCycleRemainLen>153.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000022</CrossID><StartTime>2020-03-13 17:44:49</StartTime><LastCycleLen>167.0</LastCycleLen><CurCycleLen>167.0</CurCycleLen><CurCycleRemainLen>167.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000030</CrossID><StartTime>2020-03-13 17:46:25</StartTime><LastCycleLen>78.0</LastCycleLen><CurCycleLen>78.0</CurCycleLen><CurCycleRemainLen>78.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000050</CrossID><StartTime>2020-03-13 17:46:14</StartTime><LastCycleLen>191.0</LastCycleLen><CurCycleLen>191.0</CurCycleLen><CurCycleRemainLen>191.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000011</CrossID><StartTime>2020-03-13 09:29:50</StartTime><LastCycleLen>173.0</LastCycleLen><CurCycleLen>173.0</CurCycleLen><CurCycleRemainLen>173.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000028</CrossID><StartTime>2020-03-13 17:46:02</StartTime><LastCycleLen>151.0</LastCycleLen><CurCycleLen>151.0</CurCycleLen><CurCycleRemainLen>151.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000055</CrossID><StartTime>2020-03-13 17:46:38</StartTime><LastCycleLen>159.0</LastCycleLen><CurCycleLen>159.0</CurCycleLen><CurCycleRemainLen>159.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000049</CrossID><StartTime>2020-03-13 17:44:50</StartTime><LastCycleLen>152.0</LastCycleLen><CurCycleLen>152.0</CurCycleLen><CurCycleRemainLen>152.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000033</CrossID><StartTime>2020-03-13 17:45:15</StartTime><LastCycleLen>146.0</LastCycleLen><CurCycleLen>146.0</CurCycleLen><CurCycleRemainLen>146.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000026</CrossID><StartTime>2020-03-13 17:46:25</StartTime><LastCycleLen>78.0</LastCycleLen><CurCycleLen>78.0</CurCycleLen><CurCycleRemainLen>78.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000035</CrossID><StartTime>1970-01-01 08:00:00</StartTime></CrossCycle><CrossCycle><CrossID>31012000000054</CrossID><StartTime>2020-03-13 17:48:27</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000051</CrossID><StartTime>2020-03-13 17:46:19</StartTime><LastCycleLen>99.0</LastCycleLen><CurCycleLen>99.0</CurCycleLen><CurCycleRemainLen>99.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000056</CrossID><StartTime>2020-03-13 17:45:57</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000009</CrossID><StartTime>2020-03-13 17:44:08</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000007</CrossID><StartTime>2020-03-13 17:45:06</StartTime><LastCycleLen>129.0</LastCycleLen><CurCycleLen>129.0</CurCycleLen><CurCycleRemainLen>129.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000052</CrossID><StartTime>2020-03-13 17:46:09</StartTime><LastCycleLen>101.0</LastCycleLen><CurCycleLen>101.0</CurCycleLen><CurCycleRemainLen>101.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000039</CrossID><StartTime>2020-03-13 17:44:27</StartTime><LastCycleLen>156.0</LastCycleLen><CurCycleLen>156.0</CurCycleLen><CurCycleRemainLen>156.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000032</CrossID><StartTime>2020-03-13 17:48:19</StartTime><LastCycleLen>102.0</LastCycleLen><CurCycleLen>102.0</CurCycleLen><CurCycleRemainLen>102.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000019</CrossID><StartTime>2020-03-13 17:47:40</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000059</CrossID><StartTime>2020-03-13 17:48:27</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000047</CrossID><StartTime>2020-03-13 17:45:50</StartTime><LastCycleLen>156.0</LastCycleLen><CurCycleLen>156.0</CurCycleLen><CurCycleRemainLen>156.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000012</CrossID><StartTime>2020-03-13 14:45:55</StartTime><LastCycleLen>109.0</LastCycleLen><CurCycleLen>109.0</CurCycleLen><CurCycleRemainLen>109.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000066</CrossID><StartTime>2020-03-13 17:48:09</StartTime><LastCycleLen>74.0</LastCycleLen><CurCycleLen>74.0</CurCycleLen><CurCycleRemainLen>74.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000001</CrossID><StartTime>2020-03-13 17:48:10</StartTime><LastCycleLen>156.0</LastCycleLen><CurCycleLen>156.0</CurCycleLen><CurCycleRemainLen>156.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000045</CrossID><StartTime>2020-03-13 17:45:54</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000044</CrossID><StartTime>1970-01-01 08:00:00</StartTime></CrossCycle><CrossCycle><CrossID>31012000000002</CrossID><StartTime>2020-03-13 17:47:26</StartTime><LastCycleLen>132.0</LastCycleLen><CurCycleLen>132.0</CurCycleLen><CurCycleRemainLen>132.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000014</CrossID><StartTime>2020-03-13 17:45:51</StartTime><LastCycleLen>160.0</LastCycleLen><CurCycleLen>160.0</CurCycleLen><CurCycleRemainLen>160.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000031</CrossID><StartTime>2020-03-13 17:47:45</StartTime><LastCycleLen>78.0</LastCycleLen><CurCycleLen>78.0</CurCycleLen><CurCycleRemainLen>78.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000023</CrossID><StartTime>2020-03-13 17:47:55</StartTime><LastCycleLen>171.0</LastCycleLen><CurCycleLen>171.0</CurCycleLen><CurCycleRemainLen>171.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000017</CrossID><StartTime>2020-03-13 17:47:47</StartTime><LastCycleLen>142.0</LastCycleLen><CurCycleLen>142.0</CurCycleLen><CurCycleRemainLen>142.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000070</CrossID><StartTime>2020-03-13 17:48:29</StartTime><LastCycleLen>90.0</LastCycleLen><CurCycleLen>90.0</CurCycleLen><CurCycleRemainLen>90.0</CurCycleRemainLen></CrossCycle><CrossCycle><CrossID>31012000000003</CrossID><StartTime>2020-03-13 17:47:26</StartTime><LastCycleLen>132.0</LastCycleLen><CurCycleLen>132.0</CurCycleLen><CurCycleRemainLen>132.0</CurCycleRemainLen></CrossCycle></Operation></Body></Message>"""
    # lane_param_data = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>C080D4B8264C6BA41899F93430853C2A32D246F7</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313174843000001</Seq><Body><Operation name="Notify" order="1"><CrossCycle><CrossID>31012000000065</CrossID><StartTime>2020-03-13 17:48:43</StartTime><LastCycleLen>100.0</LastCycleLen><CurCycleLen>100.0</CurCycleLen><CurCycleRemainLen>100.0</CurCycleRemainLen></CrossCycle></Operation></Body></Message>"""
    lane_param_data = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>C080D4B8264C6BA41899F93430853C2A32D246F7</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200313175109000001</Seq><Body><Operation name="Notify" order="1"><CrossStage><CrossID>31012000000031</CrossID><LastStageNo>1</LastStageNo><LastStageLen>45</LastStageLen><CurStageNo>2</CurStageNo><CurStageLen>33.0</CurStageLen><CurStageRemainLen>33.0</CurStageRemainLen><StartTime>2020-03-13 17:51:09</StartTime><CycleStartTime>2020-03-13 17:47:45</CycleStartTime></CrossStage></Operation></Body></Message>
"""

    # dh = DataHandler('send data queue', 'put datahub queue')
    #
    # dh.xml_parse(lane_param_data)
    # print(dh.data_type)
    # print(dh.object_type)
    # print(len(dh.recv_data_dict))
    # print(type(dh.recv_data_dict))

    # dh.data_handle()

    # dh.data_subscribe_handle()

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
    static_data_subscribe = StaticDataSubscribe('abc', '123', 'PhaseParam')
    static_data_subscribe.create_send_data()

    print(static_data_subscribe.send_data_xml)


if __name__ == '__main__':
    main()
















