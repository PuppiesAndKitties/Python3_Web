
if __name__ == '__main__':
    input_bytes = b'\xff\xfe4\x001\x003\x00 \x00i\x00s\x00 \x00i\x00n\x00.\x00' # 字节串： b'内容'
    input_characters = input_bytes.decode('utf-16')
    print(repr(input_characters))

    output_characters = 'Copy,Eagle.\n'
    output_bytes = output_characters.encode('utf-16')

    with open('eagle.txt','wb') as f :
        f.write(output_bytes)