# Implement CBC mode
> CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks.
>
> In CBC mode, each ciphertext block is added to the next plaintext block before the next call to the cipher core.
>
> The first plaintext block, which has no associated previous ciphertext block, is added to a "fake 0th ciphertext block" called the initialization vector, or IV.
>
> Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them.
>
> [The file here](source/challenge10/encrypted.txt) is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)
>
> Don't cheat.
>
> Do not use OpenSSL's CBC code to do CBC mode, even to verify your results. What's the point of even doing this stuff if you aren't going to learn from it?

A block cipher mode of operation is an algorithm that uses a block cipher like AES to encrypt data longer than a block size.

There are several cipher modes, and Cipher Block Chaining is one of them. In this mode, each block of plaintext is XOR'ed with the previous ciphertext block before being encrypted. This ensures that all blocks depend upon all the blocks processed until then. Refer to the Wikipedia article on [CBC mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC) to learn more. The first block is XOR'ed with an Initialization Vector (IV) to keep all blocks unique. Initialization vectors are a whole different area of cryptography themselves, and present some interesting problems. Refer to the Wikipedia article on [Initialization Vectors](https://en.wikipedia.org/wiki/Initialization_vector) to learn more.

For the current challenge, the key is "YELLOW SUBMARINE", which makes the block size 16 bytes. The IV for the challenge would be a 16 byte block of ASCII 0.

```python
KEY = b'YELLOW SUBMARINE'

IV = b'\x00'*16
```
First to define the decryption function. The decryption function uses the ```pck7_unpad()``` function from [Challenge 9](Challenge9.md), the ```aes_ecb_decrypt()``` function from [Challenge 7](Challenge7.md) and the ```repeated_xor()``` function from [Challenge 5](Challenge5.md).
```python
def aes_cbc_decrypt(ciphertext, key, iv):
    blocks = [ciphertext[i:i+16] for i in xrange(0, len(ciphertext), 16)]

    previous_block = iv

    plaintext = b""
    for block in blocks:
        plaintext_block = challenge7.aes_ecb_decrypt(block, key)

        plaintext = plaintext + challenge5.repeated_xor(plaintext_block, previous_block)

        previous_block = block

    return challenge9.pkcs7_unpad(plaintext)
```
The encryption function is defined similarly using the ```pck7_pad()``` function from [Challenge 9](Challenge9.md), the ```aes_ecb_encrypt()``` function from [Challenge 7](Challenge7.md) and the ```repeated_xor()``` function from [Challenge 5](Challenge5.md). 
```python
def aes_cbc_encrypt(plaintext, key, iv):
    padded_plaintext = challenge9.pkcs7_pad(plaintext, len(key))

    blocks = [padded_plaintext[i:i+16] for i in xrange(0, len(padded_plaintext), 16)]

    current_iv = iv

    ciphertext = b''

    for block in blocks:
        ciphertext_block = challenge5.repeated_xor(block, current_iv)

        ciphertext_block = challenge7.aes_ecb_encrypt(ciphertext_block, key)

        ciphertext = ciphertext + ciphertext_block

        current_iv = ciphertext_block

    return ciphertext
```

Now to call the decryption functions on the file.
```python
ciphertext_file = open("challenge10/encrypted.txt", "r")

ciphertext = base64.b64decode(ciphertext_file.read())

plaintext = aes_cbc_decrypt(ciphertext, KEY, IV)

print plaintext
```
