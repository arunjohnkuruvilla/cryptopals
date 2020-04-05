import string 
import re

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

character_frequencies = {
            'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339,
            'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881,
            'g': 0.0158610, 'h': 0.0492888, 'i': 0.0558094,
            'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
            'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302,
            'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563,
            's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
            'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
            'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}

def xor_string(string_to_xor, key):
	return ''.join(chr(ord(char) ^ ord(key)) for char in string_to_xor)

def chi_square_value(char, n_obs, str_len):
	return (n_obs - str_len * (character_frequencies[char]))**2/float(str_len * character_frequencies[char])


def scoring(string_to_score):
	result = 0.0
	chars_tested = []

	# if " " not in string_to_score:
	# 	return 0.0

	# if "#" in string_to_score:
	# 	return 0.0

	# if "{" in string_to_score:
	# 	return 0.0

	# if "}" in string_to_score:
	# 	return 0.0

	# if "%" in string_to_score:
	# 	return 0.0

	# if ";" in string_to_score:
	# 	return 0.0

	# if "$" in string_to_score:
	# 	return 0.0

	# if "]" in string_to_score:
	# 	return 0.0

	# if "[" in string_to_score:
	# 	return 0.0

	# if ":" in string_to_score:
	# 	return 0.0

	# if "_" in string_to_score:
	# 	return 0.0

	# if "\\" in string_to_score:
	# 	return 0.0

	# if "@" in string_to_score:
	# 	return 0.0

	# if "/" in string_to_score:
	# 	return 0.0

	# if "~" in string_to_score:
	# 	return 0.0

	# printset = set(string.printable)
	# if not set(string_to_score).issubset(printset):
	# 	return 0.0

	for char in string_to_score:
		lower_char = char.lower()
		if lower_char in string.ascii_letters:
			if lower_char not in chars_tested:
				result = result + chi_square_value(lower_char, string_to_score.count(lower_char), len(string_to_score))
				chars_tested.append(lower_char)

	return result

def simple_scoring(string_to_score):
	result = 0.0

	# if " " not in string_to_score:
	# 	return 0.0

	# if "#" in string_to_score:
	# 	return 0.0

	# if "{" in string_to_score:
	# 	return 0.0

	# if "}" in string_to_score:
	# 	return 0.0

	# if "%" in string_to_score:
	# 	return 0.0

	# if ";" in string_to_score:
	# 	return 0.0

	# if "$" in string_to_score:
	# 	return 0.0

	# if "]" in string_to_score:
	# 	return 0.0

	# if "[" in string_to_score:
	# 	return 0.0

	# if ":" in string_to_score:
	# 	return 0.0

	# if "_" in string_to_score:
	# 	return 0.0

	# if "\\" in string_to_score:
	# 	return 0.0

	# if "@" in string_to_score:
	# 	return 0.0

	# if "/" in string_to_score:
	# 	return 0.0

	# if "~" in string_to_score:
	# 	return 0.0

	for char in string_to_score:
		lower_char = char.lower()
		if lower_char in character_frequencies.keys():
			result = result + character_frequencies[lower_char]
		else:
			result = result - 0.05

	return result/len(string_to_score)

def main():

	max_score = 0.0
	max_str = ""
	max_key = ""

	for char in string.ascii_letters:
		xored_string = xor_string(ciphertext.decode("hex"), char)
		score = simple_scoring(xored_string)
		if score > max_score:
			max_score = score
			max_str = xored_string
			max_key = char

	if max_score > 0.0:
		print "Key: " + max_key + ", Plaintext: " + max_str

if __name__ == '__main__':
	main()