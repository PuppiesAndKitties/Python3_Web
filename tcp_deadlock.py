import sys, argparse, socket


def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print('一次处理最多1024字节，来源于：', sockname)
        n = 0
        while True:
            data = sc.recv(1024)
            if not data:
                break
            output = data.decode('ascii').upper().encode('ascii')
            sc.sendall(output)
            n += len(data)
            print('\r 目前已处理%d字节' % (n), end='  ')
            sys.stdout.flush()
        print()
        sc.close()
        print('socket closed')


def client(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 15) // 16 * 16
    message = b'capitalize this!'
    print('Sending', bytecount, 'bytes of data,in chunks of 16 bytes!')
    sock.connect((host, port))
    sent = 0
    while sent < bytecount:
        sock.sendall(message)
        sent += len(message)
        print('\r 已经发送了 %d 字节的消息' % (sent), end='  ')
        sys.stdout.flush()
    print()
    sock.shutdown(socket.SHUT_WR)

    print('正在接收服务器传来的所有数据...')

    received = 0
    while True:
        data = sock.recv(42)
        if not received:
            print('第一次接收到的数据是：', repr(data))
        if not data:
            break
        received += len(data)
        print('已经接受到了 %d 字节的数据' % (received), end='  ')
    print()
    sock.close()

    if __name__ == '__main__':
        choices = {'server':server,'client':client}
        parser = argparse.AugumentParser(description ='TCP的死锁情况')
        parser.add_argument('role',choices = choices,help = 'which role to play')
        parser.add_argument('host')
        parser.add_argument('bytecount',type=int,nargs = '?',default = 16) # nargs="+"表示，如果你指定了-n选项，那么-n后面至少要跟一个参数，+表示至少一个,?表示一个或0个,*0个或多个
        parser.add_argument('-p',metavar='PORT',type=int,default = 1060)
        args = parser.parse_args()
        if args.role == 'client':
            client(args.host,args.p,args.bytecount)
        else:
            server(args.host,args.p)
