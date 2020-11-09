from server.utils import create_logger


if __name__ == '__main__':
    logger_recv = create_logger('recv')
    logger_send = create_logger('send')

    logger_recv.info('recv data')
    logger_send.info('send_data')
    logger_recv.info('recv data 122212')

















