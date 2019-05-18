import struct

def pkcs7_pad(data, block_size):
    if len(data)%block_size == 0:
        return data
    remaining_bytes = block_size - len(data)%block_size

    for x in xrange(0, remaining_bytes):
        data = data + struct.pack('B', 4)
    return data

def pkcs7_unpad(data):

    padding = data[-data[-1]:]

    return all(padding[b] == len(padding) for b in xrange(0, len(padding)))

def main():
    unpadded_data = bytearray("YELLOW SUBMARINE")

    padded_data = pkcs7_pad(unpadded_data, 20)

    print pkcs7_unpad(padded_data)

if __name__ == '__main__':
    main()
