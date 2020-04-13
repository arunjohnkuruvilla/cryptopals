# Implement PKCS#7 padding
> A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext. But we almost never want to transform a single block; we encrypt irregularly-sized messages.
>
> One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the blocksize. The most popular padding scheme is called PKCS#7.
>
> So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block. For instance,
>
> ```
> "YELLOW SUBMARINE"
> ```
>
> ... padded to 20 bytes would be:
>
> ```
> "YELLOW SUBMARINE\x04\x04\x04\x04"
> ```

**PKCS** in cryptography stands for "Public Key Cryptographic Standards", which are a group of standards developed for public-key cryptography. Refer to the cryptography.io page for [PKCS#7](https://cryptography.io/en/latest/hazmat/primitives/padding/) to learn more.

The padding function checks for the number of bytes to be appended to the string. If the length on the message is a multiple of the block size, an entire block of padding with each byte being the block size is appended to the message. 

```python
def pkcs7_pad(data, block_size):
    remaining_bytes = block_size - len(data)%block_size
    if remaining_bytes == 0:
        remaining_bytes = block_size

    for x in xrange(0, remaining_bytes):
        data = data + struct.pack('B', remaining_bytes)
    return data
```

An unpadding function is also defined as follows:
```python
def pkcs7_unpad(data):

    padding = data[-struct.unpack('B', str(data[-1]))[0]:]

    if all(ord(padding[b]) == len(padding) for b in xrange(0, len(padding))):
        return data[:-len(padding)]
    else:
        return data
```

Finally to verify the functions:
```python
unpadded_data = b'YELLOW SUBMARINE'
padded_data_test = b'YELLOW SUBMARINE\x04\x04\x04\x04'

padded_data = pkcs7_pad(unpadded_data, 20)

print padded_data == padded_data_test

print pkcs7_unpad(padded_data)
```
