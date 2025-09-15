import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def mod_inv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise Exception("Tidak ada invers")

def letter_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_letter(n):
    return chr((n % 26) + ord('A'))

def sanitize(text):
    return ''.join(ch for ch in text.upper() if ch.isalpha())

def generate_keys(p, g, x=None):
    if x is None:
        x = 2
    y = mod_exp(g, x, p)
    return (p, g, y), x

def encrypt(message, public_key, k=15):
    p, g, y = public_key
    raw = sanitize(message)
    m_nums = [letter_to_num(ch) for ch in raw]

    ciphertext = []
    a = mod_exp(g, k, p)
    for m in m_nums:
        b = (m * mod_exp(y, k, p)) % p
        ciphertext.append((a, b))
    return ciphertext

def decrypt(ciphertext, private_key, p):
    plaintext_nums = []
    for a, b in ciphertext:
        s = mod_exp(a, private_key, p)
        s_inv = mod_inv(s, p)
        m = (b * s_inv) % p
        plaintext_nums.append(m)
    return ''.join(num_to_letter(num) for num in plaintext_nums)

def main():
    p = 37
    g = 3

    public_key, private_key = generate_keys(p, g)
    
    while True:
        print("\n=== ElGamal Cipher - Terminal ===")
        print("1) Enkripsi")
        print("2) Dekripsi")
        print("0) Keluar")
        choice = input("Masukkan pilihan : ").strip()

        if choice == '0':
            print("Program sudah selesai jadi tidak perlu dicari lagi. Bye👋")
            break
        elif choice == '1':
            pt = input("Masukkan Plaintext:\n> ")
            ct = encrypt(pt, public_key)
            print("\n=== HASIL ENKRIPSI ===")
            print("Plaintext :", sanitize(pt))
            print("Public Key:", public_key)
            print("Ciphertext:", ct)
            print("(Gunakan private key untuk dekripsi ->)", private_key)
        elif choice == '2':
            try:
                raw_ct = input("Masukkan Ciphertext (format: [(a1,b1),(a2,b2),...]):\n> ")
                ct = eval(raw_ct)
                priv = int(input("Masukkan Private Key:\n> "))
                rec = decrypt(ct, priv, p)
                print("\n=== HASIL DEKRIPSI ===")
                print("Ciphertext:", ct)
                print("Recovered :", rec)
            except Exception as e:
                print("Error saat dekripsi:", e)
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()