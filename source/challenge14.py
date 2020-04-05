import os
import random
import base64
import fractions
import string

import challenge7
import challenge8
import challenge11
import challenge12

EPILOGUE = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

PROLOGUE = ""

GLOBAL_KEY = ""

BLOCK_SIZE = 16

def encryption_oracle(plaintext):
    global GLOBAL_KEY, PROLOGUE

    modified_plaintext = PROLOGUE + plaintext + base64.b64decode(EPILOGUE)

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

    return abs(current_length - previous_length)

def find_average_block_size():
    possible_block_sizes = []
    for x in xrange(0,10):
        possible_block_sizes.append(detect_block_size())

    result = possible_block_sizes[0]

    for n in xrange(1, 10):
        result = fractions.gcd(result, possible_block_sizes[n])

    return result

def detect_ecb(ciphertext, count):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    if (len(blocks) - len(set(blocks))) == count-1:
        return True
    return False

def detect_start_of_repeating_block(ciphertext, block_size):

    number_of_blocks = len(ciphertext)/block_size

    for x in xrange(0, number_of_blocks - 3):
        if (ciphertext[x * block_size : (x+1) * block_size]
            == ciphertext[(x+1) * block_size : (x+2) * block_size]
            == ciphertext[(x+2) * block_size : (x+3) * block_size]
            == ciphertext[(x+3) * block_size : (x+4) * block_size]):
            return x
    return -1

def find_prefix_length(block_size):

    prefix_block = 0

    """ To find the prefix block, two ciphertexts are encrypted using the encryption oracle. An empty string and a one
    byte message. The block where the two ciphertexts differ contains the ending of the random prefix.
    """
    ciphertext1 = encryption_oracle(b"")
    ciphertext2 = encryption_oracle(b"A")

    for i in xrange(0, len(ciphertext2), block_size):
        if ciphertext1[i:i+block_size] != ciphertext2[i:i+block_size]:
            prefix_block = i
            break

    """ To find the precise index of the random string, three identical blocks are encrypted using the encryption
    oracle. An additional character is added with every loop. The precise index can be determined when there are three
    identical blocks of ciphertext being generated.
    """
    for x in xrange(0, block_size):
        plaintext = "A" * block_size * 3 + x * "A"

        ciphertext = encryption_oracle(plaintext)

        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        if (len(blocks) - len(set(blocks))) == 2:
            return prefix_block + block_size - x

    return prefix_block

def find_next_byte(prefix_length, block_size, current_message):

    """ The length of characters to be added to align the message decrypted so that the next block can be decrypted
    """
    length_for_current_iteration = (block_size - prefix_length - (1 + len(current_message))) % block_size

    # print "Length for current prefix: " + str(prefix_length%block_size)
    # print "Length for current iteration: " + str(length_for_current_iteration)
    # print "Length for current message: " + str(len(current_message))

    current_input = b"A" * length_for_current_iteration

    real_ciphertext = encryption_oracle(current_input)

    cracking_length = prefix_length + length_for_current_iteration + len(current_message) + 1

    for char in string.printable:
        temp_ciphertext = encryption_oracle(current_input + current_message + char)

        if real_ciphertext[:cracking_length] == temp_ciphertext[:cracking_length]:
            return char

    return b''

"""Byte by byte decryption
"""
def find_byte(prefix_length):

    """Find the block length of the encryption used.
    """
    block_length = find_average_block_size()
    # print "Average Block Length: " + str(block_length)

    """Assert that the encryption method used is ECB
    """
    temp_ciphertext = encryption_oracle("A"*block_length*4)
    assert(challenge8.detect_ecb(temp_ciphertext))

    """Length of the target-bytes can be determined by encrypting an empyt string and subtracting the prefix-length of
    the random prefix being added by the encryption oracle.
    """
    hidden_text_length = len(encryption_oracle(b"")) - prefix_length
    # print "Target-bytes length: " + str(hidden_text_length)

    # print "Total length: " + str((prefix_length + hidden_text_length)%block_length)

    hidden_message = b""
    for i in xrange(0, hidden_text_length):
        hidden_message = hidden_message + find_next_byte(prefix_length, block_length, hidden_message)

    return hidden_message

def main():
    global GLOBAL_KEY, PROLOGUE

    GLOBAL_KEY = challenge11.key_generate(BLOCK_SIZE)

    PROLOGUE = os.urandom(random.randint(5,256))

    detected_block_size = find_average_block_size()
    # print "Block size detected: " + str(detected_block_size)

    prefix_length = find_prefix_length(detected_block_size)

    # print "Detected prefix length: " + str(prefix_length)

    print "Decrypted message: \n" + find_byte(prefix_length)

if __name__ == '__main__':
    main()
