import string

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

letter_frequencies = {
            'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339,
            'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881,
            'g': 0.0158610, 'h': 0.0492888, 'i': 0.0558094,
            'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
            'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302,
            'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563,
            's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
            'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
            'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}

def compute_letter_frequency(str):
    all_freq = {}
    for i in str:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1
    return all_freq

charspace = string.ascii_letters + string.digits + ",.' :\n"

def is_string_printable(str):
    for char in str:
        if char not in charspace:
            return False;
    return True

def compute_chi_square(computed_plaintext):
    chi_squared = 0

    plaintext_letter_frequency = compute_letter_frequency(computed_plaintext.lower())

    for char, frequency in plaintext_letter_frequency.iteritems():
        if char in letter_frequencies.keys():
            chi_squared = chi_squared + ((((frequency/len(computed_plaintext)) - letter_frequencies[char])**2)/float(letter_frequencies[char]))

    return chi_squared

def single_byte_xor_attack(ciphertext_to_attack):
    max_chi = 0
    max_string = ""
    max_key = 0
    for x in xrange(0, 256):
        computed_plaintext = ''.join(chr(ord(char)^x) for char in ciphertext_to_attack.decode("hex"))

        if not is_string_printable(computed_plaintext):
            continue

        chi_squared_for_plaintext = compute_chi_square(computed_plaintext)

        if chi_squared_for_plaintext > max_chi:
            max_chi = chi_squared_for_plaintext
            max_string = computed_plaintext
            max_key = x

    return {"plaintext": max_string, 'key': hex(max_key), 'score': max_chi}

if __name__ == '__main__':
    print single_byte_xor_attack(ciphertext)
