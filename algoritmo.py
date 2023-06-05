import hashlib
import os

def generate_key(length):
    key = os.urandom(length)
    return key

def hash_key(key):
    hashed_key = hashlib.sha512(key).digest()
    return hashed_key

def encrypt(message, key):
    encrypted_message = bytearray(message)
    key_length = len(key)
    steps = []  # Almacenar los pasos del procedimiento
    for i, char in enumerate(encrypted_message):
        # Operación XOR antes de la encriptación
        char ^= key[i % key_length]
        steps.append(f"XOR con clave: {char}")
        char += key[i % key_length]
        steps.append(f"Suma con clave: {char}")
        char %= 256
        steps.append(f"Módulo 256: {char}")
        encrypted_message[i] = char
    return bytes(encrypted_message), steps

def decrypt(encrypted_message, key):
    decrypted_message = bytearray(encrypted_message)
    key_length = len(key)
    steps = []  # Almacenar los pasos del procedimiento
    for i, char in enumerate(decrypted_message):
        # Operación XOR antes de la desencriptación
        char = (char - key[i % key_length]) % 256
        steps.append(f"XOR con clave: {char}")
        char ^= key[i % key_length]
        steps.append(f"Suma con clave: {char}")
        decrypted_message[i] = char
    return bytes(decrypted_message), steps

def encrypt_message(message):
    key_length = len(message)  # Longitud de la clave igual a la longitud del mensaje
    key = generate_key(key_length)  # Generar la clave aleatoria
    hashed_key = hash_key(key)  # Obtener la clave hash
    encrypted_message, steps = encrypt(message, hashed_key)
    return encrypted_message, hashed_key, steps

def decrypt_message(encrypted_message, key):
    decrypted_message, steps = decrypt(encrypted_message, key)
    return decrypted_message, steps
