from server.datahub_handler import DatahubHandler


if __name__ == '__main__':

    topic_name = 'ods_devc_signal_info_gb1049_fengxian'

    dh_handler = DatahubHandler()

    data_list = [['123', 'abc', '20200312', '310000'],
                 ['456', 'hah', '20200312', '310000'],
                 ['789', 'LALA', '20200312', '310000'],
                 ]

    dh_handler.put_data(topic_name, data_list)





