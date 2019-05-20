import base64
import string
import challenge7
import challenge8
import challenge9
import challenge11

EPILOGUE = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

GLOBAL_KEY = ""

BLOCK_SIZE = 16

def encryption_oracle(plaintext):
    global GLOBAL_KEY

    modified_plaintext =  plaintext + base64.b64decode(EPILOGUE)

    return challenge7.aes_ecb_encrypt(modified_plaintext, GLOBAL_KEY)

def detect_block_size():
    temp_input = b""

    detected_block_size = 0
    previous_length = len(encryption_oracle(temp_input))
    current_length = 0
    for x in xrange(0,10000):
        temp_input = temp_input + b"A"
        current_length = len(encryption_oracle(temp_input))
        if current_length == previous_length:
            continue
        else:
            break

    return current_length - previous_length

def main():
    global GLOBAL_KEY

    GLOBAL_KEY = challenge11.key_generate(BLOCK_SIZE)

    detected_block_size = detect_block_size()
    print "Block size detected: " + str(detected_block_size)

    assert(challenge8.detect_ecb(encryption_oracle(b"A" * 64)))

    padding = ""

    for i in xrange(0,len(encryption_oracle(b""))):
        detected = ""
        for x in xrange(1, detected_block_size + 1):
            plaintext = b"A"*(detected_block_size - x)

            ciphertext = encryption_oracle(plaintext)

            for char in string.printable:
                detected_block = encryption_oracle(b"A"*(detected_block_size - x) + padding + detected + char)
                if detected_block[0:len(padding)+16] == ciphertext[0:len(padding)+16]:
                    detected = detected + char
                    break
        padding = padding + detected

    assert(base64.b64decode(EPILOGUE) == challenge9.pkcs7_unpad(padding))

if __name__ == '__main__':
    main()
