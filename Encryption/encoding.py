import numpy as np
import random
from sympy import randprime
from math import gcd

# --- Diffie-Hellman Functions ---
def generate_dh_params(bit_length=2048):
    """Generates Diffie-Hellman parameters."""
    p = randprime(2**(bit_length - 1), 2**bit_length)
    g = 2  # Using 2 as the generator for simplicity
    return p, g

def generate_dh_private_key(p):
    """Generates a private key for Diffie-Hellman."""
    return random.randint(2, p - 2)

def generate_dh_public_key(p, g, private_key):
    """Generates a public key for Diffie-Hellman."""
    return pow(g, private_key, p)

def compute_dh_shared_secret(p, other_public_key, private_key):
    """Computes the shared secret using Diffie-Hellman."""
    return pow(other_public_key, private_key, p)

# --- RSA Functions ---
def generate_rsa_keys(bit_length=2048):
    """Generates RSA public and private keys."""
    p = randprime(2**(bit_length - 1), 2**bit_length)
    q = randprime(2**(bit_length - 1), 2**bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537  # Use a fixed public exponent for better efficiency and security
    
    d = pow(e, -1, phi)  # Modular inverse of e
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def rsa_encrypt_string(public_key, message):
    """Encrypts a string message using RSA."""
    e, n = public_key
    message_bytes = message.encode('utf-8')
    message_int = int.from_bytes(message_bytes, 'big')
    encrypted_int = pow(message_int, e, n)
    return encrypted_int

def rsa_decrypt_string(private_key, ciphertext):
    """Decrypts an RSA-encrypted string."""
    d, n = private_key
    decrypted_int = pow(ciphertext, d, n)
    decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
    return decrypted_bytes.decode('utf-8')



# --- Hill Cipher Functions ---
def text_to_numbers(text):
    """Converts plaintext to a list of numbers."""
    text = ''.join(filter(str.isalpha, text.upper()))
    return [ord(char) - ord('A') for char in text]

def numbers_to_text(numbers):
    """Converts a list of numbers back to text."""
    return ''.join(chr((num % 26) + ord('A')) for num in numbers)

def pad_text(numbers, block_size):
    """Pads text to be a multiple of the block size."""
    padding_length = block_size - (len(numbers) % block_size)
    if padding_length < block_size:
        numbers.extend([25] * padding_length)  # Pad with 'Z' = 25
    return numbers

def remove_padding(text):
    """Removes padding from text."""
    return text.rstrip('Z')

def is_invertible_mod26(matrix):
    """Checks if a matrix is invertible modulo 26."""
    det = int(round(np.linalg.det(matrix))) % 26
    return det != 0 and np.gcd(det, 26) == 1

def mod_inverse(a, m):
    """Finds the modular inverse of a under modulo m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse for {a} under modulo {m}")

def compute_modular_inverse(matrix, mod):
    """Computes the modular inverse of a matrix."""
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det, mod)
    adj = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)).astype(int) % mod
    return (det_inv * adj) % mod

def hill_encrypt(plaintext, key):
    """Encrypts plaintext using the Hill cipher."""
    if not plaintext or not isinstance(plaintext, str):
        raise ValueError("Invalid plaintext")
    if not is_invertible_mod26(key):
        raise ValueError("Key matrix is not invertible modulo 26")
    
    plaintext_numbers = text_to_numbers(plaintext)
    block_size = key.shape[0]
    plaintext_numbers = pad_text(plaintext_numbers, block_size)
    
    blocks = len(plaintext_numbers) // block_size
    plaintext_matrix = np.array(plaintext_numbers).reshape(blocks, block_size).T
    ciphertext_matrix = np.dot(key, plaintext_matrix) % 26
    ciphertext_numbers = ciphertext_matrix.T.flatten()
    return numbers_to_text(ciphertext_numbers)

def hill_decrypt(ciphertext, key):
    """Decrypts ciphertext using the Hill cipher."""
    if not ciphertext or not isinstance(ciphertext, str):
        raise ValueError("Invalid ciphertext")
    if not is_invertible_mod26(key):
        raise ValueError("Key matrix is not invertible modulo 26")
    
    ciphertext_numbers = text_to_numbers(ciphertext)
    block_size = key.shape[0]
    if len(ciphertext_numbers) % block_size != 0:
        ciphertext_numbers = pad_text(ciphertext_numbers, block_size)
    
    blocks = len(ciphertext_numbers) // block_size
    ciphertext_matrix = np.array(ciphertext_numbers).reshape(blocks, block_size).T
    
    key_inv = compute_modular_inverse(key, 26)
    plaintext_matrix = np.dot(key_inv, ciphertext_matrix) % 26
    plaintext_numbers = plaintext_matrix.T.flatten()
    plaintext = numbers_to_text(plaintext_numbers)
    return remove_padding(plaintext)

# --- Testing ---
def test_encryption_algorithms():
    """Tests all implemented encryption algorithms."""
    KEY = np.array([
        [6, 24, 1],
        [13, 16, 10],
        [20, 17, 15]
    ]) % 26
    
    print("=== Hill Cipher ===")
    test_cases = ["HELLO", "CRYPTOGRAPHY", "TEST", "HILL CIPHER"]
    for test in test_cases:
        encrypted = hill_encrypt(test, KEY)
        decrypted = hill_decrypt(encrypted, KEY)
        print(f"Original: {test}, Encrypted: {encrypted}, Decrypted: {decrypted}")

    print("\n=== ElGamal Encryption ===")
    p = 7919  # A large prime number
    public_key, private_key = generate_elgamal_keys(p)
    message = "Hello, ElGamal!"
    ciphertext = elgamal_encrypt(public_key, message)
    decrypted = elgamal_decrypt(private_key, public_key, ciphertext)
    print(f"Message: {message}, Ciphertext: {ciphertext}, Decrypted: {decrypted}")

    print("\n=== RSA Encryption ===")
    public_key, private_key = generate_rsa_keys(bit_length=2048)
    message = "Hello, RSA!"
    ciphertext = rsa_encrypt_string(public_key, message)
    decrypted = rsa_decrypt_string(private_key, ciphertext)
    print(f"Message: {message}, Ciphertext: {ciphertext}, Decrypted: {decrypted}")

    print("\n=== Diffie-Hellman Key Exchange ===")
    # Generate Diffie-Hellman parameters
    p, g = generate_dh_params()
    
    # Alice's keys
    alice_private = generate_dh_private_key(p)
    alice_public = generate_dh_public_key(p, g, alice_private)
    
    # Bob's keys
    bob_private = generate_dh_private_ss