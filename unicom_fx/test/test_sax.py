import xml.sax.handler
import pprint


class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping

data = """<?xml version="1.0" encoding="UTF-8"?>
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
  <Seq>20140829084311000015</Seq>
  <Body>
    <Operation order="1" name="Get">
      <SysInfo>
        <SysName>智能交通管控平台</SysName>
        <SysVersion>3.04</SysVersion>
        <Supplier>XXXXXX</Supplier>
        <RegionIDList>
	  <RegionID>330100211</RegionID>
<RegionID>330100212</RegionID>
        </RegionIDList>
        <SignalControlerIDList>
	  <SignalControlerID>33010058792223258</SignalControlerID>
     <SignalControlerID>33010058792223259</SignalControlerID>
        </SignalControlerIDList>
      </SysInfo>
    </Operation>
  </Body>
</Message>
"""

xh = XMLHandler()
xml.sax.parseString(data.strip().encode(), xh)
ret = xh.getDict()

pprint.pprint(ret)



