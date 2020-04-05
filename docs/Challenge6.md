# Break repeating-key XOR

> It is officially on, now.
>
> This challenge isn't conceptually hard, but it involves actual error-prone coding. The other challenges in this set are there to bring you up to speed. This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.
>
> [There's a file here](source/challenge6/encrypted.txt). It's been base64'd after being encrypted with repeating-key XOR.
>
> Decrypt it.
>
> Here's how:
>
> 1. Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
>
> 2. Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:
>
>  ```
>  this is a test
>  ```
>  and
>
>  ```
>  wokka wokka!!!
>  ```
>  is **37**. Make sure your code agrees before you proceed.
> 3. For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
>
> 4. The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
> 5. Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
>
> 6. Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
> 7. Solve each block as if it was single-character XOR. You already have code to do this.
> 8. For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
>
> This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.
>
> No, that's not a mistake.
>
> We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors in this text. In particular: the "wokka wokka!!!" edit distance really is 37.

First, define a function to compute hamming distance between two strings.
```python
def hamming_distance(str1, str2):
	if len(str1) != len(str2):
		return 0
	else:
		result = 0

		for char1, char2 in zip(str1, str2):
			result = result + bin(ord(char1) ^ ord(char2)).count("1")
		return result
```

Next step is to identify the key size. The ```find_key_size()``` takes 12 chunks of the ciphertext, with each chunk varying in length between 2 and 41, and computes the highest average hamming distance for each chunk size. The function then sorts the sizes in decreasing order of hamming distances and returns a dictionary.

```python
def find_key_sizes(ciphertext):
    key_distances = {}

    for key_size in xrange(2,41):
        str_part_1 = ciphertext[0:key_size]
        str_part_2 = ciphertext[key_size:key_size*2]

        str_part_3 = ciphertext[key_size*2:key_size*3]
        str_part_4 = ciphertext[key_size*3:key_size*4]

        str_part_5 = ciphertext[key_size*4:key_size*5]
        str_part_6 = ciphertext[key_size*5:key_size*6]

        str_part_7 = ciphertext[key_size*6:key_size*7]
        str_part_8 = ciphertext[key_size*7:key_size*8]

        str_part_9 = ciphertext[key_size*8:key_size*9]
        str_part_10 = ciphertext[key_size*9:key_size*10]

        str_part_11 = ciphertext[key_size*10:key_size*11]
        str_part_12 = ciphertext[key_size*11:key_size*12]

        # key_distances[key_size] = (hamming_distance(str_part_1, str_part_2))/float(key_size)
        key_distances[key_size] = ((hamming_distance(str_part_1, str_part_2) + hamming_distance(str_part_3, str_part_4)+ hamming_distance(str_part_5, str_part_6) + hamming_distance(str_part_7, str_part_8) + hamming_distance(str_part_9, str_part_10) + hamming_distance(str_part_11, str_part_12))/float(key_size))/6

    sorted_key_distances = sorted(key_distances.items(), key=lambda kv: kv[1])
```

A function to compute the transpose of a string is also defined.
```python
def transpose(text, size):
	output = {}

	for i in xrange(size):
		output[i] = ''

	for count, char in enumerate(text):
		output[count%size] = output[count%size] + char

	return output
```
Next, the ciphertext is read from the file and base64 decoded. After identifying the key size, the ciphertext is transposed by breaking up the string as per the key size. Then, all keys are looped over and XOR'ed with each block. For each key, the best chi_squared value is considered as a potential key byte. All individually identified key bytes are combined to recreate the key. The ciphertext is then repeating-key XOR'ed with the key to get the plaintext. 

```python
assert hamming_distance("this is a test", "wokka wokka!!!") == 37

min_key_size = 10000

f = open("challenge6/encrypted.txt", "r")

ciphertext = base64.b64decode(f.read())

sorted_key_distances = find_key_sizes(ciphertext)

for key_pair in sorted_key_distances[0:1]:
    print key_pair
    key_result = ""
    for key, block in transpose(ciphertext, key_pair[0]).iteritems():
        max_score = 0
        max_key = ''
        for char in string.printable:
            computed_plaintext = challenge5.repeated_xor(block, char)

            score = challenge3.compute_chi_square(computed_plaintext)

            if score > max_score:
                max_score = score
                max_key = char

        key_result = key_result + max_key

    print challenge5.repeated_xor(ciphertext, key_result)
    print "KEY: " + key_result
```
