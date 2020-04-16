# AES in ECB mode

> The Base64-encoded content [in this file](../source/challenge7/encrypted.txt) has been encrypted via AES-128 in ECB mode under the key
>
> ```
> "YELLOW SUBMARINE".
> ```
> (case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).
>
> Decrypt it. You know the key, after all.
>
> Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
>
> Do this with code.
>
> You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for a reason. You'll need it a lot later on, and not just for attacking ECB.

The Advanced Encryption Standard (AES), is a block cipher used for encryption. AES is a symmetric encryption algorithm, and both parties talking must share the same key beforehand. Refer to the Wikipedia article on [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) to learn more.

Electronic Code Book (ECB) is the simplest way of applying the AES algorithm on a message. This involves splitting the message into equal sized blocks and applying the algorithm on each block.

For this challenge, the [PyCrypto package](https://www.dlitz.net/software/pycrypto/api/current/) is used for crypto functionality. As a rule of thumb, steer away from implementing cryptographic algorithms yourself. As much as possible use well documented public cryptographic implementations only.

The decryption function:
```python
from Crypto.Cipher import AES

def aes_ecb_decrypt(plaintext, key):
    obj = AES.new(key, AES.MODE_ECB)
    return obj.encrypt(plaintext)
```

The data for the file is read and passed on to this function:
```python
import base64
...
KEY = "YELLOW SUBMARINE"

f = open("challenge7/encrypted.txt", "r")
ciphertext = base64.b64decode(f.read())

print aes_ecb_decrypt(ciphertext, KEY)
```

The source code can be found at [source/challenge7.py](source/challenge7.py).
