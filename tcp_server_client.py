#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #REFUSEADDR表示允许多个实例绑定同一个端口。详细来说，其可以指明应用程序能够使用一些网络客户端之前的连接正在关闭的端口。
    sock.bind((interface, port))        #将服务器与该端口绑定，并且interface指明了服务器要监听的网络接口。如果是localhost的话，那么表示服务器不会接收到来自其他机器的连接请求，不会有任何响应。
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())     #peer指的客户端
        message = recvall(sc, 16)
        print('  Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print('  Reply sent, socket closed')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))     #与服务器的socket进行连接（隐藏了三次握手的细节部分），连接后即可通过该socket进行通信。
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()

if __name__ == '__main__':              #argparse在主函数运行部分调用。另外，注意choices和function部分，要会使用。
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,help='TCP port (default 1060)')#前面有-或者--的表示可选值。在命令行运行程序时可以省略该项参数的
                                                                        # 填写而是选择使用默认值，# 也可以使用想要使用的值metavar是参数的名字，在显示帮助信息的时候才会用到。
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
