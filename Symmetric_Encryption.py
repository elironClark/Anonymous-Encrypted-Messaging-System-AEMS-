from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# Step 1: Generate a random AES key
key = b'Sixteen byte key'  # 128-bit key for AES

# Step 2: Encrypt the message
def encrypt_message(message, key=key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()  # Concatenate and encode for transmission

# Step 3: Decrypt the message (for receiving side)
def decrypt_message(encoded_message, key=key):
    decoded_message = base64.b64decode(encoded_message)
    nonce, tag, ciphertext = decoded_message[:16], decoded_message[16:32], decoded_message[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

