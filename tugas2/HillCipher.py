import numpy as np

def mod_inv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Tidak ada invers dari {a} mod {m}")

def text_to_numbers(text):
    return [ord(c) - ord('A') for c in text.upper() if c.isalpha()]

def numbers_to_text(nums):
    return ''.join(chr(n + ord('A')) for n in nums)

def chunk_text(text, size):
    nums = text_to_numbers(text)
    if len(nums) % size != 0:
        nums += [0] * (size - (len(nums) % size))
    return [nums[i:i+size] for i in range(0, len(nums), size)]

def hill_encrypt(plaintext, key_matrix):
    size = len(key_matrix)
    chunks = chunk_text(plaintext, size)
    cipher_nums = []
    for block in chunks:
        vec = np.array(block).reshape(size, 1)
        res = np.dot(key_matrix, vec) % 26
        cipher_nums.extend(res.flatten())
    return numbers_to_text(cipher_nums)

def hill_decrypt(ciphertext, key_matrix):
    size = len(key_matrix)
    det = int(round(np.linalg.det(key_matrix))) % 26
    det_inv = mod_inv(det, 26)
    key_inv = det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)
    key_inv = key_inv % 26

    chunks = chunk_text(ciphertext, size)
    plain_nums = []
    for block in chunks:
        vec = np.array(block).reshape(size, 1)
        res = np.dot(key_inv, vec) % 26
        plain_nums.extend(res.flatten())
    return numbers_to_text(plain_nums)

if __name__ == "__main__":
    key = np.array([[3, 3],
                    [2, 5]])
    
    while True:
        print("\n=== Hill Cipher Menu ===")
        print("1. Encrypt")
        print("2. Decrypt")
        print("0. Selesai")
        choice = input("Pilih menu: ")
        
        if choice == "1":
            plaintext = input("Masukkan plaintext: ")
            ciphertext = hill_encrypt(plaintext, key)
            print("Ciphertext:", ciphertext)
        
        elif choice == "2":
            ciphertext = input("Masukkan ciphertext: ")
            decrypted = hill_decrypt(ciphertext, key)
            print("Plaintext :", decrypted)
        
        elif choice == "0":
            print("Program selesai.")
            break
        
        else:
            print("Pilihan tidak valid!")