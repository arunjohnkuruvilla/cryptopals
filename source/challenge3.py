import string

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

letter_frequencies = {
'a':0.08167,
'b':0.01492,
'c':0.02202,
'd':0.04253,
'e':0.10270,
'f':0.02228,
'g':0.02015,
'h':0.06094,
'i':0.06966,
'j':0.00153,
'k':0.01292,
'l':0.04025,
'm':0.02406,
'n':0.06749,
'o':0.07507,
'p':0.01929,
'q':0.00095,
'r':0.05987,
's':0.06327,
't':0.09356,
'u':0.02758,
'v':0.00978,
'w':0.02560,
'x':0.00150,
'y':0.01994,
'z':0.00077
}

def compute_letter_frequency(str):
    all_freq = {}
    for i in str:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1
    return all_freq

charspace = string.ascii_letters + string.digits + ",.' "

def is_string_printable(str):
    for char in str:
        if char not in charspace:
            return False;
    return True

def compute_chi_square(computed_plaintext):
    chi_squared = 0

    if not is_string_printable(computed_plaintext):
        return 0

    plaintext_letter_frequency = compute_letter_frequency(computed_plaintext.lower())

    for char, frequency in plaintext_letter_frequency.iteritems():
        if char in letter_frequencies.keys():
            chi_squared = chi_squared + ((((frequency/len(computed_plaintext)) - letter_frequencies[char])**2)/float(letter_frequencies[char]))

    return chi_squared

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
