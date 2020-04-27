# Byte-at-a-time ECB decryption (Simple)
> Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).
>
> Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:
>
> ```
> Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
> aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
> dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
> YnkK
> ```
> Spoiler alert.
> Do not decode this string now. Don't do it.
>
> Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don't know its contents.
>
> What you have now is a function that produces:
>
> ```
> AES-128-ECB(your-string || unknown-string, random-key)
```
> It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!
>
> Here's roughly how:
>
> 1. Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
> 2. Detect that the function is using ECB. You already know, but do this step anyways.
> 3. Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
> 4. Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
> 5. Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string.
> 6. Repeat for the next byte.
>
>Congratulations.
>
>This is the first challenge we've given you whose solution will break real crypto. Lots of people know that when you encrypt something in ECB mode, you can see penguins through it. Not so many of them can decrypt the contents of those ciphertexts, and now you can. If our experience is any guideline, this attack will get you code execution in security tests about once a year.

For this challenge, the same randomly generated key is used throughout. The ```key_generate()``` function from [Challenge 11](Challenge11.md) is used to generate the key.
```python
EPILOGUE = ("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    "YnkK")

BLOCK_SIZE = 16

GLOBAL_KEY = challenge11.key_generate(BLOCK_SIZE)
```

Next the encryption oracle is defined. The encryption oracle takes the encryption key and appends the text to be identified to any message given to the oracle. The combined plaintext is then encrypted using the encryption key and returned.
```python
def encryption_oracle(plaintext):
    global GLOBAL_KEY

    modified_plaintext =  plaintext + base64.b64decode(EPILOGUE)

    return challenge7.aes_ecb_encrypt(modified_plaintext, GLOBAL_KEY)
```

The next step is to define a function that detects the block size. First an empty string is passed to the oracle to get the length of the data being appended by the oracle. Next "A" is encrypted, then "AA" is encrypted, and so on. On encrypting each string, the new length is compared with the length of the empty string ciphertext.

Assume that the length of the hidden data is 10 bytes and the hidden block size is 16. When an empty string is provided to the oracle, the oracle appends the hidden data, which is then padded to be 16 bytes. The resulting ciphertext is also 16 bytes long. This informtation is recorded.  

Now, when "A" is provided to the encryption oracle, "A" is appended with the hidden data, making the plaintext length 11. This is then padded to 16 bytes length, causing a ciphertext length of 16 bytes again. So there is no difference in length of the ciphertext.

This goes until the plaintext is "AAAAAAA" of length 7. Now, the combined length of the plaintext is 17 (7 bytes of "AAAAAAA" + 10 bytes of hidden data). This plaintext gets padded to be 32 bytes (to make the length a multiple of the block size). This in turn results in a ciphertext length of 32. This jump helps identify the block size.
```python
def detect_block_size():
    temp_input = b""

    detected_block_size = 0
    initial_length = len(encryption_oracle(temp_input))
    current_length = 0
    for x in xrange(0,10000):
        temp_input = temp_input + b"A"
        current_length = len(encryption_oracle(temp_input))
        if current_length == initial_length:
            continue
        else:
            break

    return current_length - initial_length
```

The next step is the core part of breaking the ECB mode of encryption.

Assume that the epilogue attached to the input by the oracle is "BCDEFGHI", and the block size is 4.

In the first round, a string "AAA" (string of length blocksize - 1) is provided to the encryption oracle by calling ```encryption_oracle("AAA")```. The oracle appends the epilogue, and returns the ciphertext for "AAABCDEFGHI". Now the ```identify_unkown_padding()``` function creates the following table:
```
1. encryption_oracle(AAA+A) => ciphertext(AAA+A+BCDEFGHI)
2. encryption_oracle(AAA+B) => ciphertext(AAA+B+BCDEFGHI)
3. encryption_oracle(AAA+C) => ciphertext(AAA+C+BCDEFGHI)
...
```
Since this is the first block iteration, the one block size of bytes of ```encryption_oracle("AAA")``` is compared with the table of all characters, and ```encryption_oracle("AAAB")``` is identical. Now the first byte is identified as "B".

Next the string "AAB" ((string of length blocksize - 1) + (length of bytes already identified = 3) is first provided to the encryption_oracle by calling ```encryption_oracle("AAB")```. Now the ```identify_unkown_padding()``` function creates the following table:
```
1. encryption_oracle(AAB+A) => ciphertext(AAB+A+BCDEFGHI)
2. encryption_oracle(AAB+B) => ciphertext(AAB+B+BCDEFGHI)
3. encryption_oracle(AAB+C) => ciphertext(AAB+C+BCDEFGHI)
...
```
Since this is the first block iteration, the one block size of bytes of ```encryption_oracle("AAB")``` is compared with the table of all characters, and ```encryption_oracle("AABC")``` is identical. Now the first byte is identified as "C". This makes the identified string as "BC".

Skipping over two rounds, the identified string becomes "BCDE". Now to round 2.

In round 2, the string "AAABCDE" ((string of length blocksize - 1) + (length of bytes already identified = 4) is first provided to the encryption_oracle by calling ```encryption_oracle("AAABCDE")```. Now the ```identify_unkown_padding()``` function creates the following table:
```
1. encryption_oracle(AAABCDE+A) => ciphertext(AAABCDE+A+BCDEFGHI)
2. encryption_oracle(AAABCDE+B) => ciphertext(AAABCDE+B+BCDEFGHI)
3. encryption_oracle(AAABCDE+C) => ciphertext(AAABCDE+C+BCDEFGHI)
4. encryption_oracle(AAABCDE+D) => ciphertext(AAABCDE+D+BCDEFGHI)
5. encryption_oracle(AAABCDE+E) => ciphertext(AAABCDE+E+BCDEFGHI)
6. encryption_oracle(AAABCDE+F) => ciphertext(AAABCDE+F+BCDEFGHI)
...
```
Since this is the second block iteration, the one block size of bytes of ```encryption_oracle("AAABCDE")``` is compared with the table of all characters, and ```encryption_oracle("AAABCDEF")``` is identical. Now the byte is identified as "F". This makes the identified string as "BCDEF".

This loop is followed till the entire epilogue has been identified.

```python
def identify_unkown_padding(detected_block_size):
    unknown_padding = ""

    for i in xrange(0,len(encryption_oracle(b""))):
        detected = ""
        for x in xrange(1, detected_block_size + 1):
            plaintext = b"A"*(detected_block_size - x)

            ciphertext = encryption_oracle(plaintext)

            for char in string.printable:
                detected_block = encryption_oracle(b"A"*(detected_block_size - x) + unknown_padding + detected + char)
                if detected_block[0:len(unknown_padding)+16] == ciphertext[0:len(unknown_padding)+16]:
                    detected = detected + char
                    break
        unknown_padding = unknown_padding + detected
```

Now to string all the functions together.

```python
detected_block_size = detect_block_size()
print "Block size detected: " + str(detected_block_size)

assert(challenge8.detect_ecb(encryption_oracle(b"A" * 64)))

unknown_padding = identify_unkown_padding(detected_block_size)

assert(base64.b64decode(EPILOGUE) == challenge9.pkcs7_unpad(unknown_padding))
```
