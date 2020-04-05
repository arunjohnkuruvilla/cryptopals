from Crypto.Cipher import AES
import base64
import challenge9

def aes_ecb_encrypt(plaintext, key):
    obj = AES.new(key, AES.MODE_ECB)

    ciphertext = obj.encrypt(challenge9.pkcs7_pad(plaintext, len(key)))

    return ciphertext

def aes_ecb_decrypt(ciphertext, key):
    obj = AES.new(key, AES.MODE_ECB)

    plaintext = obj.decrypt(ciphertext)

    return challenge9.pkcs7_unpad(plaintext)

def main():
    KEY = "YELLOW SUBMARINE"

    f = open("challenge7/encrypted.txt", "r")

    ciphertext = base64.b64decode(f.read())
    print ciphertext

    print aes_ecb_decrypt(ciphertext, KEY)

if __name__ == '__main__':
    main()
