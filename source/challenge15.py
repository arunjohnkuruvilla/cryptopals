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
        raise ValueError("Invalid padding.")

def main():

    str_1 = "ICE ICE BABY"

    valid_padded_string = pkcs7_pad(str_1, 16)

    assert(pkcs7_unpad(valid_padded_string) == str_1)

    invalid_padded_string = str_1

    remaining_bytes = 16 - len(str_1)%16

    for x in xrange(0, remaining_bytes):
        invalid_padded_string = invalid_padded_string + struct.pack('B', 5)

    try:
        pkcs7_unpad(invalid_padded_string)
    except ValueError as e:
        print e


    invalid_padded_string_2 = str_1 + struct.pack('B', 1) + struct.pack('B', 2) + struct.pack('B', 3) + struct.pack('B', 4)

    try:
        pkcs7_unpad(invalid_padded_string_2)
    except ValueError as e:
        print e

if __name__ == '__main__':
    main()
