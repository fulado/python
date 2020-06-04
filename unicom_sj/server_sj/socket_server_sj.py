"""
主程序
"""
import sys
sys.path.append('/opt/unicom_sj')

from socketserver import TCPServer

from server_sj.request_handler import MyRequestHandler


def main():
    address = '', 19527

    tcp_server = TCPServer(address, MyRequestHandler)
    print('等待客户端连接...')

    try:
        tcp_server.serve_forever()  # 服务器永远等待客户端的连接
    except KeyboardInterrupt:
        tcp_server.server_close()   # 关闭服务器套接字
        print('Close')


if __name__ == '__main__':
    main()
