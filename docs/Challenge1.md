# Convert hex to base64

> ```
> 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d```
>
> Should produce:
>
> ```
> SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
>```
>
> So go ahead and make that happen. You'll need to use this code for the rest of the exercises.
>
> Cryptopals Rule
> Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.

Base64 encoding is a an encoding format where every base64 character is used to encode 6 bits of information (2<sup>6</sup> = 64). Hex encoding is an encoding format where every character encodes 4 bits of information (2<sup>4</sup> = 16). Both forms of encoding are used to print raw bytes in readable form. However base64 encoding results in a smaller string length as compared to hex encoding. Refer to the Wikipedia article for more information about [base64](https://en.wikipedia.org/wiki/Base64) and [hex](https://en.wikipedia.org/wiki/Hexadecimal) encoding.

First the original string is decoded to raw bytes:

```python
raw_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d".decode("hex")
```

Next, the string is base64 encoded:
```python
import base64
...
base64_string = base64.b64encode(raw_string)
```

The [base64 module](https://docs.python.org/2/library/base64.html) in python is used to convert the hex encoded string to a base64 encoded string.

The base64 encoded string is then compared with the final string.

```python
print(base64_string == SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t)
```
