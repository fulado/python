from server_2.data_handler import DataHandler


def main():
    xml_data = """
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

    data_handler.xml_parse(xml_data)
    print(data_handler.object_type)
    print(data_handler.recv_data_dict)

    # data = data_handler.recv_data_dict.get('StageNoList').keys()
    # print(list(data))
    # for k, v in data_handler.recv_data_dict.items():
    #     print(k, v)


if __name__ == '__main__':
    main()
















