# Fixed XOR

> Write a function that takes two equal-length buffers and produces their XOR combination.
>
> If your function works properly, then when you feed it the string:
>
> ```
> 1c0111001f010100061a024b53535009181c
> ```
> ... after hex decoding, and when XOR'd against:
>
> ```
> 686974207468652062756c6c277320657965
> ```
> ... should produce:
>
> ```
> 746865206b696420646f6e277420706c6179
> ```

XOR is a logical operation between two bits which results in a 1 if both the bits are different, and a 0 if both the bits are the same. Refer to the Wikipedia article to learn for about the [XOR operation](https://en.wikipedia.org/wiki/Exclusive_or).

Bitwise XOR in python is done using the ^ operation. First, the two strings to be XOR'ed are converted to raw bytes.

```python
raw_string_1 = "1c0111001f010100061a024b53535009181c".decode("hex")
raw_string_2 = "686974207468652062756c6c277320657965".decode("hex")
```

The following function takes two strings and XOR'ed byte by byte:
```python
def xor_strings(str1, str2):
    return ''.join(chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(str1, str2))
```

The two input strings are XOR'ed using the function defined above:
```python
xored_raw_string = xor_strings(raw_string_1, raw_string_2)
```
The result is encoded back to hex to be compared with the the final string:

```python
print(xored_raw_string.encode("hex") == "746865206b696420646f6e277420706c6179")
```
The entire code can be found at [source/challenge2.py](source/challenge2.py)
