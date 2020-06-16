# encoding:utf-8

from server_2.data_handler import DataHandler
from static_data.static_data import StaticData
from command.cmd_result import CmdResult


recv_data_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<Message>
  <Version>1.0</Version>
  <Token>02FCB106FB8742B0901E14BAFB0DD4B0411D5B82</Token>
  <From>
    <Address>
      <Sys>UTCS</Sys>
      <SubSys/>
      <Instance/>
    </Address>
  </From>
  <To>
    <Address>
      <Sys>TICP</Sys>
      <SubSys/>
      <Instance/>
    </Address>
  </To>
  <Type>RESPONSE</Type>
  <Seq>20200612105752000708</Seq>
  <Body>
    <Operation name="Set" order="6">
      <SDO_Error>
        <ErrObj>TEMPPLANPARAM</ErrObj>
        <ErrType>SDE_Failure</ErrType>
        <ErrDesc>操作失败</ErrDesc>
      </SDO_Error>
      <TempPlanParam>
        <CrossID>31012000000044</CrossID>
        <CoordStageNo>null</CoordStageNo>
        <OffSet>57</OffSet>
        <EndTime>2020-06-12 16:30:00</EndTime>
        <SplitTimeList>
          <SplitTime>
            <StageNo/>
            <Green>34</Green>
          </SplitTime>
          <SplitTime>
            <StageNo/>
            <Green>80</Green>
          </SplitTime>
          <SplitTime>
            <StageNo/>
            <Green>30</Green>
          </SplitTime>
        </SplitTimeList>
      </TempPlanParam>
    </Operation>
  </Body>
</Message>
"""
data_handler = DataHandler('123456', 'send data queue', 'put datahub queue')
data_handler.xml_parse(recv_data_xml.strip())

print(data_handler.data_type)
print(data_handler.object_type)
print(data_handler.recv_data_dict)
print(data_handler.error_data)

# cmd_result = CmdResult('RESPONSE')
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














