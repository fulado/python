"""
主程序
"""

from socketserver import TCPServer, ThreadingTCPServer


from server_2.request_handler import MyRequestHandler


def main():
    address = '', 19530

    tcp_server = TCPServer(address, MyRequestHandler)
    print('等待客户端连接...')

    try:
        tcp_server.serve_forever()  # 服务器永远等待客户端的连接
    except KeyboardInterrupt:
        tcp_server.server_close()   # 关闭服务器套接字
        print('Close')


if __name__ == '__main__':
    main()
