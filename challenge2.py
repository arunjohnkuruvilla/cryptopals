string1 = r'1c0111001f010100061a024b53535009181c'
string2 = r'686974207468652062756c6c277320657965'

final = r'746865206b696420646f6e277420706c6179'

def xor(str1, str2):
	return ''.join(chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(str1, str2))

def main():
	print final == xor(string1.decode("hex"), string2.decode("hex")).encode("hex")

if __name__ == '__main__':
	main()