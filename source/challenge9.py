import struct

def pkcs7_pad(data, block_size):
    remaining_bytes = block_size - len(data)%block_size
    if remaining_bytes == 0:
        remaining_bytes = block_size

    for x in xrange(0, remaining_bytes):
        data = data + struct.pack('B', remaining_bytes)
    return data

def pkcs7_unpad(data):

    padding = data[-struct.unpack('B', str(data[-1]))[0]:]

    if all(ord(padding[b]) == len(padding) for b in xrange(0, len(padding))):
        return data[:-len(padding)]
    else:
        return data

def main():
    unpadded_data = b'YELLOW SUBMARINE'

    padded_data_test = b'YELLOW SUBMARINE\x04\x04\x04\x04'

    padded_data = pkcs7_pad(unpadded_data, 20)

    print len(padded_data)

    print padded_data == padded_data_test

    print pkcs7_unpad(padded_data)

if __name__ == '__main__':
    main()
