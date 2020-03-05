from server_2.data_handler import DataHandler


def main():
    xml_data = """
    <?xml version="1.0" encoding="UTF-8"?>
    <Message>
      <Version>1.2</Version>
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
      <Seq>20140829084311000001</Seq>
      <Body>
        <Operation order="1" name="Get">
          <LaneParam>
            <CrossID>33010021133250</CrossID>
            <LaneNo>1</LaneNo>
            <Direction>1</Direction>
            <Attribute>1</Attribute>
            <Movement>11</Movement>
            <Feature>1</Feature>
          </LaneParam>
        </Operation>
      </Body>
    </Message>
    """

    data_handler = DataHandler('send data queue')

    data_handler.xml_parse(xml_data)
    print(data_handler.object_type)
    print(data_handler.recv_data_dict)

    # for k, v in data_handler.recv_data_dict.items():
    #     print(k, v)


if __name__ == '__main__':
    main()
















