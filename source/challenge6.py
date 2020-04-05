import binascii
import base64
import challenge3
import challenge5
import string
import sys

def hamming_distance(str1, str2):
	if len(str1) != len(str2):
		return 0
	else:
		result = 0

		for char1, char2 in zip(str1, str2):
			result = result + bin(ord(char1) ^ ord(char2)).count("1")
		return result
	
def transpose(text, size):
	output = {}

	for i in xrange(size):
		output[i] = ''

	for count, char in enumerate(text):
		output[count%size] = output[count%size] + char

	return output

def main():
	assert hamming_distance("this is a test", "wokka wokka!!!") == 37

	min_key_size = 10000

	f = open("challenge6/encrypted.txt", "r")

	ciphertext = base64.b64decode(f.read())

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

	for key_pair in sorted_key_distances[0:1]:
		key_result = ""
		for key, block in transpose(ciphertext, key_pair[0]).iteritems():
			max_score = 0
			max_key = ''
			for char in string.printable:
				score = challenge3.simple_scoring(challenge3.xor_string(block, char))
				if score > max_score:
					max_score = score
					max_key = char
			key_result = key_result + max_key

		print challenge5.repeated_xor(ciphertext, key_result)
		# print key_result

if __name__ == '__main__':
	main()