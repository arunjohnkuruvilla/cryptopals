# Detect single-character XOR
> One of the 60-character strings in this [file](source/challenge4/encrypted.txt) has been encrypted by single-character XOR.
>
> Find it.
>
> (Your code from #3 should help.)

For this challenge, the character space of the plaintext is extended to include new line.

```python
CHARACTER_SPACE = string.ascii_letters + string.digits + ",.' :\n"
```
The next steps are straight-forward, with calling the ```single_byte_xor_attack()``` function on each ling of the file.

```python
import challenge3

f = open("challenge4/encrypted.txt", "r")

max_score = 0
max_str = ""
max_key = 0
line_found = 0

for counter, ciphertext in enumerate(f.readlines()):
    result = challenge3.single_byte_xor_attack(ciphertext.strip())

    if result["score"] > max_score:
        max_score = result["score"]
        max_str = result["plaintext"]
        max_key = result["key"]
        line_found = counter

print "Line #" + str(line_found) + ", Key: " + str(max_key) + ", Plaintext: " + max_str
```
