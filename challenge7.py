from Crypto.Cipher import AES
import base64

def aes_ecb_decrypt(ciphertext, key):
    obj = AES.new(key, AES.MODE_ECB)

    plaintext = obj.decrypt(ciphertext)

    return plaintext

def main():
    KEY = "YELLOW SUBMARINE"

    f = open("challenge7/encrypted.txt", "r")

    ciphertext = base64.b64decode(f.read())

    print aes_ecb_decrypt(ciphertext, KEY)

if __name__ == '__main__':
    main()
