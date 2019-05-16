from Crypto.Cipher import AES
import base64

key = "YELLOW SUBMARINE"

f = open("challenge7/encrypted.txt", "r")

ciphertext = base64.b64decode(f.read())

obj = AES.new(key, AES.MODE_ECB)

plaintext = obj.decrypt(ciphertext)

print plaintext
