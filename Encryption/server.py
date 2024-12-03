import socket
import threading
import json

clients = {}  # Dictionary to store client sockets and their names
public_keys = {}  # Dictionary to store public keys for each client
clients_lock = threading.Lock()  # Lock for synchronizing access to clients and public_keys

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")

    client_name = receive_client_name(client_socket)
    if not client_name:
        return

    with clients_lock:
        if client_name in clients.values():
            client_socket.send("Name already taken. Please choose another.".encode())
            client_socket.close()
            return
        clients[client_socket] = client_name

    broadcast(f"{client_name} has joined the chat.", None)
    send_client_list()

    while True:
        try:
            message = client_socket.recv(4096).decode()
            if not message:
                break

            print(f"DEBUG: Server received: {message}")

            if message.startswith("PUBLIC_KEY"):
                handle_public_key(client_name, message)
            elif message.startswith("KEY_RECEIVED"):
                _, receiver, sender = message.split(":")
                forward_key_receipt(receiver, sender)
            elif message.startswith("REQUEST_KEY"):
                _, requested_client = message.split(":")
                request_public_key(client_name, requested_client)
            elif message == "REQUEST_ALL_KEYS":
                broadcast_all_keys(client_name)
            elif message.startswith("BROADCAST"):
                _, encrypted_content = message.split(" ", 1)
                broadcast_message = f"BROADCAST {client_name} {encrypted_content}"
                broadcast(broadcast_message, client_socket)
            elif message.startswith("PRIVATE"):
                _, recipient_name, encrypted_content = message.split(" ", 2)
                private_message = f"PRIVATE {client_name} {encrypted_content}"
                send_private_message(recipient_name, private_message)
            elif message == "REQUEST_CLIENT_LIST":
                send_client_list(client_socket)
            elif message.startswith("DELETE_CLIENT"):
                _, client_to_delete = message.split(" ", 1)
                delete_client(client_to_delete)
            else:
                print(f"Unknown message format: {message}")

        except Exception as e:
            print(f"Error handling message from {client_name}: {e}")
            break

    cleanup_client(client_socket, client_name)

def receive_client_name(client_socket):
    try:
        return client_socket.recv(1024).decode()
    except Exception as e:
        print(f"Error receiving client name: {e}")
        client_socket.close()
        return None

def handle_public_key(client_name, message):
    try:
        _, _, encryption_method, *key_parts = message.split(":")
        key_data = ":".join(key_parts)
        public_keys[client_name] = {"method": encryption_method, "key": key_data}
        print(f"Received public key from {client_name}: {public_keys[client_name]}")
        broadcast_public_key(client_name, encryption_method, key_data)
    except Exception as e:
        print(f"Error handling public key from {client_name}: {e}")

def broadcast_public_key(client_name, encryption_method, key_data):
    message = f"PUBLIC_KEY:{client_name}:{encryption_method}:{key_data}"
    broadcast(message, None)

def forward_key_receipt(receiver, sender):
    message = f"KEY_RECEIVED:{receiver}:{sender}"
    with clients_lock:
        for client_socket, name in clients.items():
            if name == sender:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error forwarding key receipt: {e}")

def request_public_key(requester, requested_client):
    message = f"REQUEST_KEY:{requester}"
    with clients_lock:
        for client_socket, name in clients.items():
            if name == requested_client:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error requesting public key: {e}")

def broadcast_all_keys(requesting_client):
    with clients_lock:
        for client_socket, name in clients.items():
            if name != requesting_client:
                try:
                    client_socket.send(f"REQUEST_KEY:{requesting_client}".encode())
                except Exception as e:
                    print(f"Error broadcasting key request: {e}")

def broadcast(message, sender_socket):
    with clients_lock:
        for client_socket in list(clients.keys()):
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error broadcasting message: {e}")
                    client_socket.close()
                    del clients[client_socket]

def send_client_list(requesting_socket=None):
    client_list = "\n".join(clients.values())
    target_sockets = [requesting_socket] if requesting_socket else clients.keys()

    with clients_lock:
        for client_socket in target_sockets:
            try:
                client_socket.send(f"CLIENT_LIST\n{client_list}".encode())
            except Exception as e:
                print(f"Error sending client list: {e}")
                client_socket.close()
                if client_socket in clients:
                    del clients[client_socket]

def send_private_message(recipient_name, message):
    found = False
    with clients_lock:
        for client_socket, name in clients.items():
            if name == recipient_name:
                try:
                    client_socket.send(message.encode())
                    found = True
                    break
                except Exception as e:
                    print(f"Error sending private message: {e}")
                    client_socket.close()
                    del clients[client_socket]
    if not found:
        print(f"Recipient {recipient_name} not found.")

def delete_client(client_name):
    with clients_lock:
        for client_socket, name in list(clients.items()):
            if name == client_name:
                try:
                    client_socket.send("You have been removed from the chat.".encode())
                    client_socket.close()
                    del clients[client_socket]
                    if client_name in public_keys:
                        del public_keys[client_name]
                    broadcast(f"{client_name} has been removed from the chat.", None)
                    send_client_list()
                    return
                except Exception as e:
                    print(f"Error deleting client {client_name}: {e}")
    print(f"Client {client_name} not found for deletion.")

def cleanup_client(client_socket, client_name):
    with clients_lock:
        if client_socket in clients:
            del clients[client_socket]
            if client_name in public_keys:
                del public_keys[client_name]
            broadcast(f"{client_name} has left the chat.", None)
            send_client_list()
    client_socket.close()
    print(f"Connection from {client_socket.getpeername()} closed")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8082))
    server_socket.listen()
    print("Server is listening on port 8082")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
