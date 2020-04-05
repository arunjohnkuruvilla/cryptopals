import string
import challenge3
import base64
import re

import binascii

def xor_string(string_to_xor, key):
	return ''.join(chr(ord(char) ^ ord(key)) for char in string_to_xor)

def main():
	max_max_score = 0.0
	max_max_str = ""
	max_max_key = ""

	f = open("challenge4/encrypted.txt", "r")

	for ciphertext in f.readlines():
		max_score = 0.0
		max_str = ""
		max_key = ""

		for char in string.printable:
			xored_string = xor_string(binascii.unhexlify(ciphertext.strip()), char)

			for ch in xored_string:
				if ch not in string.printable:
					continue

			score = challenge3.simple_scoring(xored_string)

			if score > max_score:
				max_score = score
				max_str = xored_string
				max_key = char

		if max_score > max_max_score:
			max_max_score = max_score
			max_max_str = max_str
			max_max_key = max_key

	if max_max_score > 0.0:
		print "Key: " + max_max_key + ": " + max_max_str
		

if __name__ == '__main__':
	main()