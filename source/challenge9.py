import struct

def pkcs7_pad(data, block_size):
    if len(data)%block_size == 0:
        return data
    remaining_bytes = block_size - len(data)%block_size

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
    unpadded_data = r"YELLOW SUBMARINE"

    padded_data = pkcs7_pad(unpadded_data, 20)

    print pkcs7_unpad(padded_data)

if __name__ == '__main__':
    main()
