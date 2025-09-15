import string

ALPHABET = string.ascii_uppercase
A_ORD = ord('A')

def letter_to_num(c):
    return ord(c) - A_ORD

def num_to_letter(n):
    return chr((n % 26) + A_ORD)

def sanitize(text):
    return ''.join(ch for ch in text.upper() if ch.isalpha())

def repeat_key(key, length):
    key = sanitize(key)
    if not key:
        raise ValueError("Key harus mengandung minimal satu huruf.")
    return (key * ((length // len(key)) + 1))[:length]

def print_table(columns, header_names):
    rows = len(columns[0])
    cols = len(columns)
    col_width = 4

    left_label_width = max(len(lbl) for lbl in header_names) + 1
    index_row = " " * (left_label_width) + "|"
    for i in range(cols):
        index_row += f" {i+1:^{col_width-1}}|"
    print(index_row)
    print("-" * (left_label_width + (col_width * cols) + cols + 1))

    for r, label in enumerate(header_names):
        row_str = f"{label:<{left_label_width}}|"
        for c in range(cols):
            cell = columns[c][r]
            row_str += f" {cell:^{col_width-1}}|"
        print(row_str)
    print()

def encrypt_vigenere(plaintext, key):
    raw = sanitize(plaintext)
    if not raw:
        raise ValueError("Plaintext harus mengandung minimal satu huruf A-Z.")
    key_rep = repeat_key(key, len(raw))

    cols = []
    ct_chars = []
    for pch, kch in zip(raw, key_rep):
        n_pt = letter_to_num(pch)
        n_k = letter_to_num(kch)
        n_sum = (n_pt + n_k) % 26
        cch = num_to_letter(n_sum)
        cols.append([pch, str(n_pt), kch, str(n_k), str(n_sum), cch])
        ct_chars.append(cch)

    print("=== TABEL ENKRIPSI VIGENÈRE ===")
    row_labels = ["PT", "n(PT)", "K", "n(K)", "(n(PT)+n(K)) mod26", "CT"]
    print_table(cols, row_labels)

    ciphertext = ''.join(ct_chars)
    print(f"Plaintext : {plaintext}")
    print(f"Key : {sanitize(key)}")
    print(f"Ciphertext : {ciphertext}")
    return ciphertext

def decrypt_vigenere(ciphertext, key):
    raw = sanitize(ciphertext)
    if not raw:
        raise ValueError("Ciphertext harus mengandung minimal satu huruf A-Z.")
    key_rep = repeat_key(key, len(raw))

    cols = []
    pt_chars = []
    for cch, kch in zip(raw, key_rep):
        n_ct = letter_to_num(cch)
        n_k = letter_to_num(kch)
        n_pt = (n_ct - n_k + 26) % 26
        pch = num_to_letter(n_pt)
        cols.append([cch, str(n_ct), kch, str(n_k), str(n_pt), pch])
        pt_chars.append(pch)

    print("=== TABEL DEKRIPSI VIGENÈRE ===")
    row_labels = ["CT", "n(CT)", "K", "n(K)", "(n(CT)-n(K)+26) mod26", "PT"]
    print_table(cols, row_labels)

    plaintext = ''.join(pt_chars)
    print(f"Ciphertext : {ciphertext}")
    print(f"Key : {sanitize(key)}")
    print(f"Recovered Plaintext: {plaintext}")
    return plaintext

def main():
    while True:
        print("\n=== Vigenere Cipher - Terminal ===")
        print("1) Enkripsi")
        print("2) Dekripsi")
        print("0) Keluar")
        choice = input("Masukkan pilihan : ").strip()

        if choice == '0':
            print("Program sudah selesai jadi tidak perlu dicari lagi. Bye👋")
            break
        elif choice == '1':
            pt = input("Masukkan Plaintext:\n> ")
            key = input("Masukkan Key:\n> ")
            try:
                encrypt_vigenere(pt, key)
            except ValueError as e:
                print("Error:", e)
        elif choice == '2':
            ct = input("Masukkan Ciphertext:\n> ")
            key = input("Masukkan Key:\n> ")
            try:
                decrypt_vigenere(ct, key)
            except ValueError as e:
                print("Error:", e)
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()