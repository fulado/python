import socket


class SocketServer(object):
    def __init__(self):
        self.port = 19530
        self.buffer = '1024'

    def start(self):
        # 创建
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEADDR, 1)
        address = ('', self.port)
        socket_server.bind(address)
        socket_server.listen(5)

        try:
            while True:
                print('-----主进程，，等待新客户端的到来------')
                new_socket, client_addr = socket_server.accept()

                print('-----主进程，，接下来创建一个新的进程负责数据处理[%s]-----' % str(client_addr))
                # 处理客户端请求
        except Exception as e:
            print(e)









