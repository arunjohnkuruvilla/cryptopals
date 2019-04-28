import string 

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

character_frequencies = {
	'a':8.167,	
	'b':1.492,	
	'c':2.782,	
	'd':4.253,	
	'e':12.702,	
	'f':2.228,	
	'g':2.015,	
	'h':6.094,	
	'i':6.966,	
	'j':0.153,	
	'k':0.772,	
	'l':4.025,	
	'm':2.406,	
	'n':6.749,	
	'o':7.507,	
	'p':1.929,	
	'q':0.095,	
	'r':5.987,	
	's':6.327,	
	't':9.056,	
	'u':2.758,	
	'v':0.978,	
	'w':2.360,	
	'x':0.150,	
	'y':1.974,	
	'z':0.074
}

def xor_string(string, key):
	return ''.join(chr(ord(char) ^ ord(key)) for char in string)

def chi_square_value(char, n_obs, str_len):
	return (n_obs + str_len * character_frequencies[char])**2/float(str_len * character_frequencies[char])


def scoring(string_to_score):
	result = 0.0
	chars_tested = []

	for char in string_to_score:
		lower_char = char.lower()
		if lower_char in string.ascii_letters:
			if lower_char not in chars_tested:
				result = result + chi_square_value(lower_char, string_to_score.count(lower_char), len(string_to_score))
				chars_tested.append(lower_char)

	return result


def main():

	max_score = 0.0
	max_str = ""
	max_key = ""

	for char in string.ascii_letters:
		xored_string = xor_string(ciphertext.decode("hex"), char)
		score = scoring(xored_string)
		if score > max_score:
			max_score = score
			max_str = xored_string
			max_key = char

	if max_score > 0.0:
		print "Key: " + max_key + ", Plaintext: " + max_str

if __name__ == '__main__':
	main()