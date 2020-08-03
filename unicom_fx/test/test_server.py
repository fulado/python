from socketserver import TCPServer, BaseRequestHandler


# 创建 StreamRequestHandler 类的子类
class MyRequestHandler(BaseRequestHandler):
    # 重写 handle 方法，该方法在父类中什么都不做
    def setup(self):
        print('建立连接')
        print(self.client_address)

    def handle(self):
        try:
            while True:
                print('接收数据')
                request_data = self.request.recv(100000)
                print(request_data)

                response_data = 'Got it'
                self.request.send(response_data.encode())
        except Exception as e:
            print(e)

    def finish(self):
        print('关闭连接')
        self.request.close()


def main():
    address = '127.0.0.1', 19530

    tcp_server = TCPServer(address, MyRequestHandler)
    print('等待客户端连接...')

    try:
        tcp_server.serve_forever()  # 服务器永远等待客户端的连接
    except KeyboardInterrupt:
        tcp_server.server_close()   # 关闭服务器套接字
        print('\nClose')


if __name__ == '__main__':
    main()



