"""
主程序
"""
from server.socket_server import SocketServer


if __name__ == '__main__':
    s_server = SocketServer()
    s_server.start()
