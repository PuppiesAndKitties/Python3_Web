import socket,struct

header_struct = struct.Struct('!I')  # messages up to 2**32 - 1 in length
print (header_struct.size)
def recvall(sock,length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left in this blcok'.format(length))
        length -= len(block)
        blocks.append(block)
        return b''.join(blocks)

def get_block(sock):
    data = recvall(sock,header_struct.size)
    (block_length,) = header_struct.unpack(data)
    return recvall(sock,block_length)

def put_block(sock,message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))
    sock.send(message)

def server(address):
    print('server running...')
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(address)
    sock.listen(1)
    print('listening at ',sock.getsockname)
    sc,sockname = sock.accept()
    print('Accepted connection from',sockname)
    sc.shutdown(socket.SHUT_WR)
    while True:
        block = get_block(sc)
        if not block:
            break
        print('Block''s content is:',repr(block))
    sc.close()
    sock.close()

def client(address):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    put_block(sock,b'1st messageaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    put_block(sock,b'2nd message sdfdsfasdfdsafdsa adfs adsf asdf ')
    put_block(sock,b'3rd message sdakh;lykhl;kdfghfdg')
    put_block(sock,b'')
    sock.close()

if __name__ == "__main__":
    address = ('127.0.0.1',8080)
    #server(address)
    #client(address)
