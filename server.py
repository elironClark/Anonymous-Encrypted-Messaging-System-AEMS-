import threading
import socket
from Symmetric_Encryption import encrypt_message, decrypt_message  # Import encryption functions

host = '0.0.0.0'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []

# Function to broadcast a message to the chat, encrypting it first
def broadcast(message):
    encrypted_message = encrypt_message(message)  # Encrypt the message before sending
    for client in clients:
        client.send(encrypted_message.encode('utf-8'))


# Function to handle clients' connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            decrypted_message = decrypt_message(message)  # Decrypt incoming message
            broadcast(decrypted_message)
        except:
            # Remove client from chat
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!')
            aliases.remove(alias)
            break


# Main function to receive client connections
def receive():
    while True:
        print('Server is running and listening...')
        client, address = server.accept()
        print(f'Connection established with {str(address)}')
        
        # Handle client alias
        client.send(encrypt_message("alias?").encode('utf-8'))
        alias = decrypt_message(client.recv(1024).decode('utf-8'))
        aliases.append(alias)
        clients.append(client)
        
        # Notify others and confirm connection to client
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat room')
        client.send(encrypt_message('You are now connected!').encode('utf-8'))
        
        # Start a new thread for the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
