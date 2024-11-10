import threading
import socket
from Symmetric_Encryption import encrypt_message, decrypt_message  # Import encryption functions

alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))


def client_receive():
    while True:
        try:
            message = decrypt_message(client.recv(1024).decode('utf-8'))  # Decrypt incoming message
            if message == "alias?":
                client.send(encrypt_message(alias).encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        encrypted_message = encrypt_message(message)  # Encrypt the outgoing message
        client.send(encrypted_message.encode('utf-8'))


# Start threads for receiving and sending
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
