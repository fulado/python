import xmltodict



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
  <Type>PUSH</Type>
  <Seq>20140829084311000002</Seq>
  <Body>
    <Operation order="1" name="Notify">
      <CrossTrafficData>
		<CrossID>33010021133250</CrossID>
<EndTime>2016-07-05 09:00:00</EndTime>
       <Interval>15</Interval>
       <DataList>
<Data>
<LaneNo>1</LaneNo>
           <Volume>1</Volume>
           <AvgVehLen>1.1</AvgVehLen>
           <Pcu>11</Pcu>
           <HeadDistance>1.1</HeadDistance>
           <HeadTime>2</HeadTime>
           <Speed>1.1</Speed>
           <Saturation>1.1</Saturation>
           <Density>11</Density>
           <QueueLength>1</QueueLength>
           <Occupancy>11</Occupancy>
</Data>
</DataList>
     </CrossTrafficData>
   </Operation>
  </Body>
</Message>
"""

dict_data = xmltodict.parse(xml_data.strip())


print(dict_data)




