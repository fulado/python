from server_2.data_handler import DataHandler
from static_data.lane_param import LaneParam
from static_data.lamp_group import LaneParam


recv_data_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<Message>
  <Version>1.1</Version>
  <Token></Token>
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
  <Seq>20140829084311000019</Seq>
  <Body>
    <Operation order="1" name="Get">
      <LampGroup>
        <SignalControlerID>3301005879222325811</SignalControlerID>
        <LampGroupNo>1</LampGroupNo>
        <Direction>0</Direction>
        <Type>10</Type>
      </LampGroup>
    </Operation>
  </Body>
</Message>    
    """

data_handler = DataHandler('send data queue')
data_handler.xml_parse(recv_data_xml)

lane_param = LaneParam()
lane_param.parse_recv_data(data_handler.recv_data_dict)













