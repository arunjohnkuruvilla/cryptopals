def detect_ecb(ciphertext, blocksize=16):
    if (len(ciphertext)%blocksize) != 0:
        return False
    blocks = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]
    if len(blocks) != len(set(blocks)):
        return True
    return False

def main():
    f = open("challenge8/encrypted.txt", "r")

    result = 0

    for count, ciphertext in enumerate(f.readlines()):
        if detect_ecb(ciphertext.strip().decode("hex")):
            result = count

    print result
    assert(result == 132)

if __name__ == '__main__':
    main()
