import xmltodict

from .test_xml import xml_parse


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

dict_data = xmltodict.parse(xml_data.strip())

data = xml

print(data)




