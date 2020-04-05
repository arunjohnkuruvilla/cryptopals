import string
import challenge3
import base64

def main():
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

if __name__ == '__main__':
	main()
