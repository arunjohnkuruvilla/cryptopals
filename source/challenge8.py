def detect_ecb(ciphertext):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    if len(blocks) != len(set(blocks)):
        return True
    return False

def main():
    f = open("challenge8/encrypted.txt", "r")

    result = 0

    for count, ciphertext in enumerate(f.readlines()):
        if detect_ecb(ciphertext):
            result = count

    assert(result == 132)

if __name__ == '__main__':
    main()
