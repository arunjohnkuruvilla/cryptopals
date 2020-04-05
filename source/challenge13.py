from Crypto.Cipher import AES
from collections import OrderedDict

import challenge7
import challenge9
import challenge11
import challenge12

GLOBAL_KEY = challenge11.key_generate(AES.block_size)

def encryption_oracle(email):
    global GLOBAL_KEY

    modified_plaintext = encode(profile_for(email))

    return challenge7.aes_ecb_encrypt(modified_plaintext, GLOBAL_KEY)

def decryption_oracle(ciphertext):
    global GLOBAL_KEY

    return challenge7.aes_ecb_decrypt(ciphertext, GLOBAL_KEY)

def encode(input_dict):
    output = ""
    for element in input_dict.items():
        output = output + str(element[0]) + "=" + str(element[1]) + "&"
    return output[:-1]

def decode(input):
    output = {}
    for element in input.split("&"):
        output[element.split("=")[0]] = element.split("=")[1]
    return output

def profile_for(input):
    cleaned_input = input.replace("&", "").replace("=", "")

    output = OrderedDict()
    output['email'] = cleaned_input
    output['uid'] = 10
    output['role'] = 'user'
    return output

def create_ecb_ciphertext():
    # block1           block2                                            block3
    # email=xxxxxxxxxx admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b &uid=10&role=user

    prefix_length = AES.block_size - len("email=")
    suffix_length = AES.block_size - len("admin")

    crafted_plaintext_1 = "x" * prefix_length + "admin" + (chr(suffix_length) * suffix_length)
    crafted_ciphertext_1 = encryption_oracle(crafted_plaintext_1)

    # block1           block2           block3
    # email=asdfg.tex. com&uid=10&role= user\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c

    crafted_plaintext_2 = "asdfg.tex.com"
    crafted_ciphertext_2 = encryption_oracle(crafted_plaintext_2)

    return crafted_ciphertext_2[:32] + crafted_ciphertext_1[16:32]

def main():
    # decode("foo=bar&baz=qux&zap=zazzle")
    #
    # encryption_oracle("foo@bar.com")

    plaintext = decryption_oracle(create_ecb_ciphertext())

    assert(decode(plaintext)['role'] == "admin")

if __name__ == '__main__':
    main()
