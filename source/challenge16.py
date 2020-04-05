import struct
import base64

import challenge9
import challenge10
import challenge11
import challenge13
import challenge15

GLOBAL_KEY = ""

BLOCK_SIZE = 16

PROLOGUE = b"comment1=cooking%20MCs;userdata="

EPILOGUE = b";comment2=%20like%20a%20pound%20of%20bacon"

IV = ""

def function1(data):
    data = data.replace(";", "%3B")
    data = data.replace("=", "%3D")

    plaintext = PROLOGUE + data + EPILOGUE
    print "Plaintext: " + plaintext

    padded_plaintext = challenge9.pkcs7_pad(plaintext, BLOCK_SIZE)
    ciphertext = challenge10.aes_cbc_encrypt(padded_plaintext, GLOBAL_KEY, IV)

    return ciphertext

def function2(data):
    padded_plaintext = challenge10.aes_cbc_decrypt(data, BLOCK_SIZE, IV)

    try:
        plaintext = challenge15.pkcs7_unpad(padded_plaintext)
    except ValueError as e:
        print e
        return false

    decrypted_data = challenge13.decode(plaintext)

    if "admin" in decrypted_data:
        if decrypted_data["admin"] == "true":
            return true
    return true

def main():
    global GLOBAL_KEY, IV

    GLOBAL_KEY = challenge11.key_generate(BLOCK_SIZE)

    IV = b'\x00' * BLOCK_SIZE

    ciphertext = function1(b'asdf')

if __name__ == '__main__':
    main()
