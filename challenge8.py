f = open("challenge8/encrypted.txt", "r")

# ciphertext = f.read().decode("hex")

result = 0

for count, ciphertext in enumerate(f.readlines()):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    if len(blocks) != len(set(blocks)):
        result = count

assert(result == 132)
