import base64

cipher_text = r'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

plain_text = r'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def base64_encode(cipher_text):
	return base64.b64encode(cipher_text)

def main():
	print plain_text == base64_encode(cipher_text.decode("hex"))

if __name__ == '__main__':
	main()