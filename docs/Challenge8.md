# Detect AES in ECB mode
> [In this file](../source/challenge8/encrypted.txt) are a bunch of hex-encoded ciphertexts.
>
> One of them has been encrypted with ECB.
>
> Detect it.
>
> Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

The key to identifying the usage of ECB mode with AES is to look for identical blocks in the ciphertext. With AES being a deterministic algorithm, the same plaintext will produce the same ciphertext.

The ```has_repeated_blocks()``` function will split the ciphertext into blocks of a given size, and check if there are any repeated blocks. The presence of a repeated block indicates that the mode used was ECB.

```python
def detect_ecb(ciphertext, blocksize=16):
    if (len(ciphertext)%blocksize) != 0:
        return False
    blocks = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]
    if len(blocks) != len(set(blocks)):
        return True
    return False
```
The file content is passed line by line to the ```detect_ecb()``` function to identify the line with ECB encryption.
```python
f = open("challenge8/encrypted.txt", "r")

result = 0

for count, ciphertext in enumerate(f.readlines()):
    if detect_ecb(ciphertext.strip().decode("hex")):
        result = count

print "Line #: " + str(ciphertext)
```

The source code can be found at [source/challenge8.py](source/challenge8.py).
