import xmltodict


xml_data = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token>378184FFC3EBC542BFF7217EAC307AADC19596D0</Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>REQUEST</Type><Seq>20200302144300000001</Seq><Body><Operation name="Login" order="1"><SDO_User><UserName>fengxian</UserName><Pwd>fengxian</Pwd></SDO_User></Operation></Body></Message>"""

dict_data = xmltodict.parse(xml_data.strip())

print(dict_data)




