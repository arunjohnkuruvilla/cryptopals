import struct

def pkcs7_pad(data, block_size):
    remaining_bytes = block_size - len(data)%block_size

    if remaining_bytes == block_size:
        return data

    for x in xrange(0, remaining_bytes):
        data = data + struct.pack('B', remaining_bytes)
    return data

def pkcs7_unpad(data):
    padding_length = struct.unpack('B', str(data[-1]))[0]

    padding = data[-padding_length:]

    if all(ord(padding[b]) == len(padding) for b in xrange(0, len(padding))):
        return data[:-len(padding)]
    else:
        return data

def main():
    unpadded_data_test = b'YELLOW SUBMARINE'

    padded_data_test = b'YELLOW SUBMARINE\x04\x04\x04\x04'

    padded_data = pkcs7_pad(unpadded_data_test, 20)

    print padded_data == padded_data_test

    unpadded_data = pkcs7_unpad(padded_data)

    print unpadded_data == unpadded_data_test

if __name__ == '__main__':
    main()
