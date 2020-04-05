# Single-byte XOR cipher

> The hex encoded string:
>
>```
> 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
> ```
> ... has been XOR'd against a single character. Find the key, decrypt the message.
>
> You can do this by hand. But don't: write code to do it for you.
>
> How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
>
> Achievement Unlocked
>
> You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.

This challenge is a modified version of the famous "[Caesar Cipher](https://en.wikipedia.org/wiki/Caesar_cipher)". Instead of rotating the alphabets in a string by a fixed amount as in the case of Caesar cipher, here a single byte is XOR'ed with the entire plaintext.

The simplest attack against this encryption scheme would be to try all possible keys and identify strings that make sense in the English language. This is because the number of keys is very small. The key is a byte, which is 8 bits in length. Therefore, the total number of keys would be 256 (=2<sup>8</sup>).

```python
ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
raw_plaintext = ciphertext.decode("hex")
for x in xrange(0, 256):
    print ''.join(chr(ord(char)^x) for char in raw_plaintext)
```

This will generate 256 strings, and they have to manually inspected to identify the correct plaintext. Since the number of keys is limited, this is possible.

There are several ways the number of strings to inspect can be reduced, if there is information available about the plaintext. For example, if it is known that the plaintext is an english sentence, all computed plaintexts without a space can be ignored. Similarly, all computed plaintexts with characters not in the English alphabet can be ignored. The list goes on. After reducing plaintexts in this fashion, the next strategy would be to employ frequency analysis.

Several types of frequency analyses exist, and for this challenge the relative letter frequency analysis can be used. In English sentences, some letters are occur much more frequently than others.

```python
letter_frequencies = {
        'a':0.08167, 'b':0.01492, 'c':0.02202,
        'd':0.04253, 'e':0.10270, 'f':0.02228,
        'g':0.02015, 'h':0.06094, 'i':0.06966,
        'j':0.00153, 'k':0.01292, 'l':0.04025,
        'm':0.02406, 'n':0.06749, 'o':0.07507,
        'p':0.01929, 'q':0.00095, 'r':0.05987,
        's':0.06327, 't':0.09356, 'u':0.02758,
        'v':0.00978, 'w':0.02560, 'x':0.00150,
        'y':0.01994, 'z':0.00077
}
```

With every computed plaintext, a chi-squared test is done against the letter frequencies. A **chi-squared** test is used to determine whether there is a statistically significant difference between the expected frequencies and the observed frequencies. Refer to the Wikipedia article to learn for about the [chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test).

A character space for the plaintext will allow for easily identifying invalid characters in the computer plaintext. The string module in python is helpful in defining this. The character space can be increased to include other characters as needed. For this challenge alphabets, digits and some common punctuation symbols can be included. The ```is_string_printable()``` function will help factor out plaintexts that contain invalid characters.

```python
import string
...
CHARACTER_SPACE = string.ascii_letters + string.digits + ".,' "

def is_string_printable(str):
    for char in str:
        if char not in CHARACTER_SPACE:
            return False;
    return True
```

Another helpful function would be to calculate the count of all the characters in a computed plaintext:
```python
def compute_letter_frequency(str):
    all_freq = {}
    for i in str:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1
    return all_freq
```

For every computed plaintext, a function will compute the chi-squared value:
```python
def compute_chi_square(computed_plaintext):
    chi_squared = 0

    if not is_string_printable(computed_plaintext):
        return 0

    plaintext_letter_count = compute_letter_count(computed_plaintext.lower())

    for char, frequency in plaintext_letter_count.iteritems():
        if char in letter_frequencies.keys():
            chi_squared = chi_squared + ((((frequency/len(computed_plaintext)) - letter_frequencies[char])**2)/float(letter_frequencies[char]))

    return chi_squared
```

Finally, all the keys in the keyspace are tested to identify the most plaintext with the highest chi-squared value:
```python

def single_byte_xor_attack(ciphertext):
    max_chi = 0
    max_string = ""
    max_key = 0
    for x in xrange(0, 256):
        computed_plaintext = ''.join(chr(ord(char)^x) for char in ciphertext.decode("hex"))
        chi_squared_for_plaintext = compute_chi_square(computed_plaintext)

        if chi_squared_for_plaintext > max_chi:
            max_chi = chi_squared_for_plaintext
            max_string = computed_plaintext
            max_key = x

    return {"plaintext": max_string, 'key': hex(max_key)}

print single_byte_xor_attack(ciphertext)
```

The entire code can be found at [source/challenge3.py](source/challenge3.py)
