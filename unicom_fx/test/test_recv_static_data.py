from server_2.data_handler import DataHandler
from static_data.static_data import StaticData


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
  <Seq>20140829084311000012</Seq>
  <Body>
    <Operation order="1" name="Get">
      <PlanParam>
	<CrossID>33010021133250</CrossID>
        <PlanNo>1</PlanNo>
        <CycleLen>110</CycleLen>
        <CoordPhaseNo>1</CoordPhaseNo>
        <OffSet>1</OffSet>
        <StageNoList>
	  <StageNo>1</StageNo>
	  <StageNo>2</StageNo>
	  <StageNo>3</StageNo>
</StageNoList>
      </PlanParam>
    </Operation>
  </Body>
</Message>
    """

data_handler = DataHandler('send data queue')
data_handler.xml_parse(recv_data_xml)

static_data = StaticData('PlanParam')
static_data.parse_recv_data(data_handler.recv_data_dict)
static_data.save_data_to_file()













