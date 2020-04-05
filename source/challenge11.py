import os
import random
import challenge7
import challenge8
import challenge10

def key_generate(key_size):
    return os.urandom(key_size)

def encryption_oracle(plaintext):
    random_key = key_generate(16)

    prologue = os.urandom(random.randint(5,10))

    epilogue = os.urandom(random.randint(5,10))

    modified_plaintext = prologue + plaintext + epilogue

    choice = random.randint(0,1)

    if choice:
        return "ECB", challenge7.aes_ecb_encrypt(modified_plaintext, random_key)
    else:
        return "CBC", challenge10.aes_cbc_encrypt(modified_plaintext, random_key, os.urandom(16))

def detect_encryption(ciphertext):
    if challenge8.detect_ecb(ciphertext):
        return "ECB"
    else:
        return "CBC"

def main():
    input_data = bytes([0]*64)

    for x in xrange(0, 10):
        encryption_used, ciphertext = encryption_oracle(input_data)

        encryption_detected = detect_encryption(ciphertext)

        assert(encryption_used == encryption_detected)

if __name__ == '__main__':
    main()
