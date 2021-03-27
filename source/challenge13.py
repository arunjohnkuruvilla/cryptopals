from Crypto.Cipher import AES
from collections import OrderedDict

import challenge7
import challenge9
import challenge11
import challenge12

GLOBAL_KEY = challenge11.key_generate(AES.block_size)

def encryption_oracle(plaintext):
    global GLOBAL_KEY

    return challenge7.aes_ecb_encrypt(plaintext, GLOBAL_KEY)

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

def profile_for(input_email):
    cleaned_input = input_email.replace("&", "").replace("=", "")

    output = OrderedDict()
    output['email'] = cleaned_input
    output['uid'] = 10
    output['role'] = 'user'
    return encryption_oracle(encode(output))

def create_ecb_ciphertext():
    # block1           block2                                            block3
    # email=xxxxxxxxxx admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b &uid=10&role=user

    prefix_length = AES.block_size - len("email=")
    suffix_length = AES.block_size - len("admin")

    crafted_plaintext_1 = "x" * prefix_length + "admin" + (chr(suffix_length) * suffix_length)
    crafted_ciphertext_1 = profile_for(crafted_plaintext_1)


    # block1           block2                                           block3
    # email=xxxxxxxxxx madmin\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c   &uid=10&role=user

    # block1           block2           block3
    # email=foo@bar.co m&uid=10&role=us er\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e

    crafted_plaintext_2 = "asdfg.tex@com"
    crafted_ciphertext_2 = profile_for(crafted_plaintext_2)

    return crafted_ciphertext_2[:32] + crafted_ciphertext_1[16:32]

def main():
    # print (decode("foo=bar&baz=qux&zap=zazzle"))
    #

    ciphertext_1 = profile_for('foo@bar.com')
    plaintext_1 = decode(decryption_oracle(ciphertext_1))
    print "Key-value pair for 'foo@bar.com' - " + str(plaintext_1)

    ciphertext_2 = profile_for("foo@bar.com&role=admin")
    plaintext_2 = decode(decryption_oracle(ciphertext_2))
    print "Key-value pair for 'foo@bar.com&role=admin' - " + str(plaintext_2)


    plaintext = decryption_oracle(create_ecb_ciphertext())
    assert(decode(plaintext)['role'] == "admin")
    print "Setting role=admin - " + str(decode(plaintext))

if __name__ == '__main__':
    main()
