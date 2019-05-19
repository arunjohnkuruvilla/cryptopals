import struct
import base64
import challenge5
import challenge7
import challenge9

def aes_cbc_encrypt(plaintext, key, iv):
    padded_plaintext = challenge9.pkcs7_pad(plaintext, len(key))

    blocks = [padded_plaintext[i:i+16] for i in xrange(0, len(padded_plaintext), 16)]

    current_iv = iv

    ciphertext = ""

    for block in blocks:
        ciphertext_block = challenge5.repeated_xor(block, current_iv)

        ciphertext_block = challenge7.aes_ecb_encrypt(ciphertext_block, key)

        ciphertext = ciphertext + ciphertext_block

        current_iv = ciphertext_block

    return ciphertext

def aes_cbc_decrypt(ciphertext, key, iv):
    blocks = [ciphertext[i:i+16] for i in xrange(0, len(ciphertext), 16)]

    previous_block = iv

    plaintext = ""
    for block in blocks:
        plaintext_block = challenge7.aes_ecb_decrypt(block, key)

        plaintext = plaintext + challenge5.repeated_xor(plaintext_block, previous_block)

        previous_block = block

    return challenge9.pkcs7_unpad(plaintext)

def main():
    KEY = b"YELLOW SUBMARINE"

    IV = struct.pack('B', 0)

    ciphertext_file = open("challenge10/encrypted.txt", "r")

    ciphertext = base64.b64decode(ciphertext_file.read())

    plaintext = aes_cbc_decrypt(ciphertext, KEY, IV)

    print plaintext

if __name__ == '__main__':
    main()
