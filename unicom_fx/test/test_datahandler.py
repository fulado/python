from server_2.data_handler import DataHandler
from static_data.static_data_subscribe import StaticDataSubscribe

def main():
    xml_data = """
<?xml version="1.0" encoding="UTF-8"?><Message><Version>1.0</Version><Token></Token><From><Address><Sys>UTCS</Sys><SubSys></SubSys><Instance></Instance></Address></From><To><Address><Sys>TICP</Sys><SubSys></SubSys><Instance></Instance></Address></To><Type>REQUEST</Type><Seq>20200312111649000001</Seq><Body><Operation name="Login" order="1"><SDO_User><UserName>fengxian</UserName><Pwd>fengxian</Pwd></SDO_User></Operation></Body></Message>
    """

    dh = DataHandler('send data queue')

    dh.xml_parse(xml_data)
    print(dh.object_type)
    print(dh.recv_data_dict)

    dh.data_handle()

    # data = data_handler.recv_data_dict.get('StageNoList').keys()
    # print(list(data))
    # for k, v in data_handler.recv_data_dict.items():
    #     print(k, v)

    # dh.get_cross_id_list()
    # # print(dh.cross_id_list)
    #
    # dh.get_signal_id_list()
    # # print(dh.signal_id_list)
    #
    # for cross_id in dh.cross_id_list:
    #
    #     static_data_subscribe = StaticDataSubscribe('abc', cross_id, 'LampGroup')
    #     static_data_subscribe.create_send_data()
    #
    #     print(static_data_subscribe.send_data_xml)


if __name__ == '__main__':
    main()
















