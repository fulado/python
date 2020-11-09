import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client.connect(('15.75.15.97', 19530))
client.connect(('127.0.0.1', 19530))

sdo_heart_beat = """
<?xml version="1.0" encoding="UTF-8"?>
<Message>
<Version>1.0</Version>
<Token>12345</Token>
<From>TICP</From>
<To>UTCS</To>
<Type>PUSH</Type>
<Seq>67890</Seq>
<Body>
<Operation order="1" name="notify">
<SDO_HeartBeat/>
</Operation>
</Body>
</Message>"""

sdo_user = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>31966e64-b57f-4f5b-832a-70d2d48f819b</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>REQUEST</Type><Seq>20200603143035000001</Seq><Body><Operation name="Login" order="1"><SDO_User><UserName>fengxian</UserName><Pwd>fengxian</Pwd></SDO_User></Operation></Body></Message>
"""

# sys_info = """
# <?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>D2B7B0381E95C35E6A6E4820DA833A3DF0A89CA0</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200313105915000952</Seq><Body><Operation name="Get" order="5"><SysInfo><SysName>CSTCP4.0信号控制系统</SysName><SysVersion>1.0</SysVersion><Supplier>宝康</Supplier><RegionIDList><RegionID>310120000</RegionID></RegionIDList><SignalControlerIDList><SignalControlerID>31012000000000066</SignalControlerID><SignalControlerID>31012000000000064</SignalControlerID><SignalControlerID>31012000000000065</SignalControlerID><SignalControlerID>31012000000000067</SignalControlerID><SignalControlerID>31012000000000068</SignalControlerID><SignalControlerID>31012000000000069</SignalControlerID><SignalControlerID>31012000000000002</SignalControlerID><SignalControlerID>31012000000000001</SignalControlerID><SignalControlerID>31012000000000005</SignalControlerID><SignalControlerID>31012000000000006</SignalControlerID><SignalControlerID>31012000000000007</SignalControlerID><SignalControlerID>31012000000000008</SignalControlerID><SignalControlerID>31012000000000009</SignalControlerID><SignalControlerID>31012000000000011</SignalControlerID><SignalControlerID>31012000000000012</SignalControlerID><SignalControlerID>31012000000097055</SignalControlerID><SignalControlerID>31012000000000015</SignalControlerID><SignalControlerID>31012000000000019</SignalControlerID><SignalControlerID>31012000000000021</SignalControlerID><SignalControlerID>31012000000000022</SignalControlerID><SignalControlerID>31012000000000023</SignalControlerID><SignalControlerID>31012000000000024</SignalControlerID><SignalControlerID>31012000000000025</SignalControlerID><SignalControlerID>31012000000000026</SignalControlerID><SignalControlerID>31012000000000027</SignalControlerID><SignalControlerID>31012000000000030</SignalControlerID><SignalControlerID>31012000000000032</SignalControlerID><SignalControlerID>31012000000000033</SignalControlerID><SignalControlerID>31012000000000035</SignalControlerID><SignalControlerID>31012000000000036</SignalControlerID><SignalControlerID>31012000000000038</SignalControlerID><SignalControlerID>31012000000000013</SignalControlerID><SignalControlerID>31012000000000014</SignalControlerID><SignalControlerID>31012000000000016</SignalControlerID><SignalControlerID>31012000000000018</SignalControlerID><SignalControlerID>31012000000000028</SignalControlerID><SignalControlerID>31012000000000029</SignalControlerID><SignalControlerID>31012000000000031</SignalControlerID><SignalControlerID>31012000000000034</SignalControlerID><SignalControlerID>31012000000000037</SignalControlerID><SignalControlerID>31012000000000039</SignalControlerID><SignalControlerID>31012000000000040</SignalControlerID><SignalControlerID>31012000000000041</SignalControlerID><SignalControlerID>31012000000000042</SignalControlerID><SignalControlerID>31012000000000043</SignalControlerID><SignalControlerID>31012000000000044</SignalControlerID><SignalControlerID>31012000000000017</SignalControlerID><SignalControlerID>31012000000000045</SignalControlerID><SignalControlerID>31012000000000046</SignalControlerID><SignalControlerID>31012000000000047</SignalControlerID><SignalControlerID>31012000000000003</SignalControlerID><SignalControlerID>31012000000000004</SignalControlerID><SignalControlerID>31012000000000010</SignalControlerID><SignalControlerID>31012000000000020</SignalControlerID><SignalControlerID>31012000000000048</SignalControlerID><SignalControlerID>31012000000000049</SignalControlerID><SignalControlerID>31012000000000050</SignalControlerID><SignalControlerID>31012000000000051</SignalControlerID><SignalControlerID>31012000000000052</SignalControlerID><SignalControlerID>31012000000000053</SignalControlerID><SignalControlerID>31012000000000054</SignalControlerID><SignalControlerID>31012000000000055</SignalControlerID><SignalControlerID>31012000000000056</SignalControlerID><SignalControlerID>31012000000000057</SignalControlerID><SignalControlerID>31012000000000058</SignalControlerID><SignalControlerID>31012000000000059</SignalControlerID><SignalControlerID>31012000000000060</SignalControlerID><SignalControlerID>31012000000000061</SignalControlerID><SignalControlerID>31012000000000062</SignalControlerID><SignalControlerID>31012000000000063</SignalControlerID></SignalControlerIDList></SysInfo></Operation></Body></Message>
# """

xml_data_1 = '<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>8C9518A7AD2CB43B01F3B0EEBF6DA86287F55C6B</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>PUSH</Type><Seq>20200908060020000001</Seq><Body><Operation name="Notify" order="1"><CrossCycle><CrossID>31012000000065</CrossID><StartTime>2020-09-08 '
xml_data_2 = '06:00:20</StartTime><LastCycleLen>140.0</LastCycleLen><CurCycleLen>140.0</CurCycleLen><CurCycleRemainLen>140.0</CurCycleRemainLen></CrossCycle></Operation></Body></Message><?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>8C9518A7AD2CB43B01F3B0EEBF6DA86287F55C6B</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200908055841000040</Seq><Body><Operation name="Set" order="6"><TempPlanParam><CrossID>31012000000052</CrossID><CoordStageNo>3</CoordStageNo><OffSet>37</OffSet><EndTime>2020-09-08 07:29:00</EndTime><SplitTimeList><SplitTime><StageNo>1</StageNo><Green>86</Green></SplitTime><SplitTime><StageNo>2</StageNo><Green>56</Green></SplitTime></SplitTimeList></TempPlanParam></Operation></Body></Message><?xml version="1.0" '
xml_data_3 = 'encoding="UTF-8"?><Message><Version>1.0</Version><Token>8C9518A7AD2CB43B01F3B0EEBF6DA86287F55C6B</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200908072841000006</Seq><Body><Operation name="Set" order="6"><TempPlanParam><CrossID>31012000000052</CrossID><CoordStageNo>1</CoordStageNo><OffSet>22</OffSet><EndTime>2020-09-08 08:59:00</EndTime><SplitTimeList><SplitTime><StageNo>1</StageNo><Green>90</Green></SplitTime><SplitTime><StageNo>2</StageNo><Green>52</Green></SplitTime></SplitTimeList></TempPlanParam></Operation></Body></Message>'

try:
    # while True:
    #     cmd = input("(quit退出)>>").strip()
    #     if len(cmd) == 0:
    #         continue
    #     if cmd == "quit":
    #         break
    #     client.send(cmd.encode())
    #     cmd_res = client.recv(1024)
    #     print(cmd_res.decode())

    # for i in range(5):
    #     time.sleep(1)
    #     client.send(str(i).encode())

    # client.send(sdo_user.encode())
    # recv_data = client.recv(100000)
    # print(recv_data.decode())
    #
    # # client.send(sdo_heart_beat.encode())
    # recv_data = client.recv(100000)
    # print(recv_data.decode())
    #
    # recv_data = client.recv(100000)
    # print(recv_data.decode())
    # send_data = sdo_user.strip()
    # print('%s %s %s' % ('=' * 20, '登录', '=' * 20))
    # print(send_data)
    # print('=' * 40)
    #
    # client.send(send_data.encode())
    # recv_data = client.recv(100000)
    # print(recv_data)
    # print()
    #
    # send_data = sdo_heart_beat.strip()
    # print('%s %s %s' % ('=' * 20, '心跳', '=' * 20))
    # print(send_data)
    # print('=' * 40)
    # client.send(send_data.encode())
    # recv_data = client.recv(100000)
    # print(recv_data)
    # print()
    #
    # time.sleep(5)
    # send_data = xml_data.strip()
    # print('%s %s %s' % ('=' * 20, '数据', '=' * 20))
    # print(send_data)
    # print('=' * 40)
    # client.send(send_data.encode())
    # recv_data = client.recv(100000)
    # print(recv_data)
    # print()
    #
    # time.sleep(60)

    send_data = xml_data_1
    client.send(send_data.encode())

    send_data = xml_data_2
    client.send(send_data.encode())

    send_data = xml_data_3
    client.send(send_data.encode())

    time.sleep(10)

    # while True:
    #     recv_data = client.recv(100000)
    #     print(recv_data.decode())

except Exception as e:
    print(e)
finally:
    print('关闭连接')
    client.close()
