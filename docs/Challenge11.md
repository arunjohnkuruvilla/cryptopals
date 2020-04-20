# An ECB/CBC detection oracle
> Now that you have ECB and CBC working:
>
> Write a function to generate a random AES key; that's just 16 random bytes.
>
> Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.
>
> The function should look like:
>
> ```
> encryption_oracle(your-input)
> => [MEANINGLESS JIBBER JABBER]
> ```
> Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.
>
> Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.
>
> Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.

First, a key generation function is defined that uses the ```urandom()``` function from the [os module](https://docs.python.org/3/library/os.html#os.urandom).
```python
def key_generate(key_size):
    return os.urandom(key_size)
```

The next function defined is the random encryptor function. On every run, the function generates a new key, appends and prepends a random set of bytes, and randomly encrypts the plaintext using ECB or CBC mode. The ```random.randint()``` function in [the random module](https://docs.python.org/3/library/random.html#random.randint) is used to mimic a coin toss for picking the mode of encryption.

```python
def random_encryptor(plaintext):
    random_key = key_generate(16)

    prologue = os.urandom(random.randint(5,10))

    epilogue = os.urandom(random.randint(5,10))

    modified_plaintext = prologue + plaintext + epilogue

    choice = random.randint(0,1)

    if choice:
        return "ECB", challenge7.aes_ecb_encrypt(modified_plaintext, random_key)
    else:
        return "CBC", challenge10.aes_cbc_encrypt(modified_plaintext, random_key, os.urandom(16))
```

The next step is to define an encryption oracle. The oracle uses the ```detect_ecb()``` function from [Challenge 8](Challenge8.md).
```python
def mode_detection_oracle(ciphertext):
    if challenge8.detect_ecb(ciphertext):
        return "ECB"
    else:
        return "CBC"
```
The encryption oracle can now be tested in the following way:

```python
input_data = "A"*256

for x in xrange(0, 10):
    encryption_used, ciphertext = random_encryptor(input_data)

    encryption_detected = mode_detection_oracle(ciphertext)
    print (encryption_used == encryption_detected)
```
