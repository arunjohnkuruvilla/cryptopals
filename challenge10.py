import struct
import challenge5
import challenge7
import base64

def aes_cbc_decrypt(ciphertext, key, iv):
    blocks = [ciphertext[i:i+16] for i in xrange(0, len(ciphertext), 16)]

    previous_block = iv

    plaintext = ""
    for block in blocks:
        plaintext_block = challenge7.aes_ecb_decrypt(block, key)

        plaintext = plaintext + challenge5.repeated_xor(plaintext_block, previous_block)

        previous_block = block

    return plaintext

def main():
    KEY = b"YELLOW SUBMARINE"

    IV = struct.pack('B', 0)

    ciphertext_file = open("challenge10/encrypted.txt", "r")

    ciphertext = base64.b64decode(ciphertext_file.read())

    plaintext = aes_cbc_decrypt(ciphertext, KEY, IV)

    print plaintext

if __name__ == '__main__':
    main()
