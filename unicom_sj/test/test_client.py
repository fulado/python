import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client.connect(('15.75.15.97', 19530))
client.connect(('127.0.0.1', 19527))

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
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>31966e64-b57f-4f5b-832a-70d2d48f819b</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>REQUEST</Type><Seq>20200603143035000001</Seq><Body><Operation name="Login" order="1"><SDO_User><UserName>admin</UserName><Pwd>1qaz2wsx123456</Pwd></SDO_User></Operation></Body></Message>
"""

sys_info = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>D2B7B0381E95C35E6A6E4820DA833A3DF0A89CA0</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200313105915000952</Seq><Body><Operation name="Get" order="5"><SysInfo><SysName>CSTCP4.0信号控制系统</SysName><SysVersion>1.0</SysVersion><Supplier>宝康</Supplier><RegionIDList><RegionID>310120000</RegionID></RegionIDList><SignalControlerIDList><SignalControlerID>31012000000000066</SignalControlerID><SignalControlerID>31012000000000064</SignalControlerID><SignalControlerID>31012000000000065</SignalControlerID><SignalControlerID>31012000000000067</SignalControlerID><SignalControlerID>31012000000000068</SignalControlerID><SignalControlerID>31012000000000069</SignalControlerID><SignalControlerID>31012000000000002</SignalControlerID><SignalControlerID>31012000000000001</SignalControlerID><SignalControlerID>31012000000000005</SignalControlerID><SignalControlerID>31012000000000006</SignalControlerID><SignalControlerID>31012000000000007</SignalControlerID><SignalControlerID>31012000000000008</SignalControlerID><SignalControlerID>31012000000000009</SignalControlerID><SignalControlerID>31012000000000011</SignalControlerID><SignalControlerID>31012000000000012</SignalControlerID><SignalControlerID>31012000000097055</SignalControlerID><SignalControlerID>31012000000000015</SignalControlerID><SignalControlerID>31012000000000019</SignalControlerID><SignalControlerID>31012000000000021</SignalControlerID><SignalControlerID>31012000000000022</SignalControlerID><SignalControlerID>31012000000000023</SignalControlerID><SignalControlerID>31012000000000024</SignalControlerID><SignalControlerID>31012000000000025</SignalControlerID><SignalControlerID>31012000000000026</SignalControlerID><SignalControlerID>31012000000000027</SignalControlerID><SignalControlerID>31012000000000030</SignalControlerID><SignalControlerID>31012000000000032</SignalControlerID><SignalControlerID>31012000000000033</SignalControlerID><SignalControlerID>31012000000000035</SignalControlerID><SignalControlerID>31012000000000036</SignalControlerID><SignalControlerID>31012000000000038</SignalControlerID><SignalControlerID>31012000000000013</SignalControlerID><SignalControlerID>31012000000000014</SignalControlerID><SignalControlerID>31012000000000016</SignalControlerID><SignalControlerID>31012000000000018</SignalControlerID><SignalControlerID>31012000000000028</SignalControlerID><SignalControlerID>31012000000000029</SignalControlerID><SignalControlerID>31012000000000031</SignalControlerID><SignalControlerID>31012000000000034</SignalControlerID><SignalControlerID>31012000000000037</SignalControlerID><SignalControlerID>31012000000000039</SignalControlerID><SignalControlerID>31012000000000040</SignalControlerID><SignalControlerID>31012000000000041</SignalControlerID><SignalControlerID>31012000000000042</SignalControlerID><SignalControlerID>31012000000000043</SignalControlerID><SignalControlerID>31012000000000044</SignalControlerID><SignalControlerID>31012000000000017</SignalControlerID><SignalControlerID>31012000000000045</SignalControlerID><SignalControlerID>31012000000000046</SignalControlerID><SignalControlerID>31012000000000047</SignalControlerID><SignalControlerID>31012000000000003</SignalControlerID><SignalControlerID>31012000000000004</SignalControlerID><SignalControlerID>31012000000000010</SignalControlerID><SignalControlerID>31012000000000020</SignalControlerID><SignalControlerID>31012000000000048</SignalControlerID><SignalControlerID>31012000000000049</SignalControlerID><SignalControlerID>31012000000000050</SignalControlerID><SignalControlerID>31012000000000051</SignalControlerID><SignalControlerID>31012000000000052</SignalControlerID><SignalControlerID>31012000000000053</SignalControlerID><SignalControlerID>31012000000000054</SignalControlerID><SignalControlerID>31012000000000055</SignalControlerID><SignalControlerID>31012000000000056</SignalControlerID><SignalControlerID>31012000000000057</SignalControlerID><SignalControlerID>31012000000000058</SignalControlerID><SignalControlerID>31012000000000059</SignalControlerID><SignalControlerID>31012000000000060</SignalControlerID><SignalControlerID>31012000000000061</SignalControlerID><SignalControlerID>31012000000000062</SignalControlerID><SignalControlerID>31012000000000063</SignalControlerID></SignalControlerIDList></SysInfo></Operation></Body></Message>
"""

xml_data = """<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>D27967B2B6EF6611F8A23F846592D7A5CA861260</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>RESPONSE</Type><Seq>20200316160904000835</Seq><Body><Operation name="Get" order="5"><LaneParam><CrossID>31012000000010</CrossID><LaneNo>6</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>5</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>4</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>15</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>14</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>13</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>12</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>11</LaneNo><Direction>0</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>7</LaneNo><Direction>2</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>21</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>22</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>20</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>19</LaneNo><Direction>6</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>28</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>13</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>27</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>26</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>11</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>25</LaneNo><Direction>4</Direction><Attribute>1</Attribute><Movement>12</Movement><Feature>1</Feature></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>1</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>2</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>3</LaneNo><Direction>2</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>8</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>9</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>10</LaneNo><Direction>0</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>16</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>17</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>18</LaneNo><Direction>6</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>22</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>23</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam><LaneParam><CrossID>31012000000010</CrossID><LaneNo>24</LaneNo><Direction>4</Direction><Attribute>2</Attribute></LaneParam></Operation></Body></Message>"""


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
    send_data = sdo_user.strip()
    # print(send_data)
    client.send(send_data.encode())

    recv_data = client.recv(100000)

    # client.send(sdo_heart_beat.encode())

    # while True:
    #     recv_data = client.recv(100000)
    #     print(recv_data.decode())

except Exception as e:
    print(e)
finally:
    print('关闭连接')
    client.close()
