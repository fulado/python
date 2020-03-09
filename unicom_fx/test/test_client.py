import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
<?xml version="1.0" encoding="UTF-8"?>
<Message>
  <Version>1.0</Version>
  <Token>12345</Token>
  <From>UTCS</From>
  <To>
    <Address>
      <Sys>TICP</Sys>
      <SubSys/>
      <Instance/>
    </Address>
  </To>
  <Type>REQUEST</Type>
  <Seq>67890</Seq>
  <Body>
    <Operation order="1" name="Login">
      <SDO_User>
        <UserName>fengxian</UserName>
        <Pwd>fengxian</Pwd>
      </SDO_User>
    </Operation>
  </Body>
</Message>
"""

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

    while True:
        client.send(sdo_user.encode())
        recv_data = client.recv(100000)
        print(recv_data.decode())

        time.sleep(0.2)

except Exception as e:
    print(e)
finally:
    print('关闭连接')
    client.close()
