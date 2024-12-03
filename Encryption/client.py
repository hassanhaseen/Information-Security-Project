import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import base64
import json
import numpy as np
from sympy import randprime
import random
from encoding import hill_encrypt, hill_decrypt, rsa_encrypt_string, rsa_decrypt_string, generate_rsa_keys, generate_elgamal_keys, elgamal_encrypt, elgamal_decrypt

class ClientApp:
    def __init__(self, root, client_socket, client_name):
        self.root = root
        self.client_socket = client_socket
        self.client_name = client_name
        self.client_list = []
        self.current_selection = set()

        # Encryption variables
        self.encryption_method = "rsa"  # Default to RSA
        self.hill_key = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
        self.rsa_public_key, self.rsa_private_key = generate_rsa_keys(bit_length=2048)
        self.elgamal_public_key, self.elgamal_private_key = generate_elgamal_keys(7919)
        self.public_keys = {}
        self.shared_keys = {}

        self.root.title("Encrypted Chat Application")

        # Display client name
        self.name_label = tk.Label(root, text=f"Client: {self.client_name}", font=("Arial", 12, "bold"))
        self.name_label.pack(pady=5, anchor="w")

        # Frame for encryption method selection
        self.encryption_frame = tk.Frame(root)
        self.encryption_frame.pack(pady=5)

        self.hill_button = tk.Button(self.encryption_frame, text="Hill Cipher", command=lambda: self.set_encryption_method("hill"))
        self.hill_button.pack(side=tk.LEFT, padx=5)

        self.rsa_button = tk.Button(self.encryption_frame, text="RSA", command=lambda: self.set_encryption_method("rsa"))
        self.rsa_button.pack(side=tk.LEFT, padx=5)

        
        # Frame for Clients List and Chat Window
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Left Pane for Clients
        self.client_list_frame = tk.Frame(self.main_frame, width=200, bg='lightgrey')
        self.client_list_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.client_listbox = tk.Listbox(self.client_list_frame, width=25, selectmode=tk.MULTIPLE)
        self.client_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.client_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        # Right Pane for Chat Window
        self.chat_frame = tk.Frame(self.main_frame)
        self.chat_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_window.pack(fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(self.chat_frame, width=50)
        self.msg_entry.pack(pady=10, side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(pady=10, side=tk.RIGHT)

        # Menu Button
        self.menu_button = tk.Button(root, text="Menu", command=self.show_menu)
        self.menu_button.pack(pady=10)

        # Request the client list on startup
        self.view_clients()

        # Broadcast public key after a short delay
        self.root.after(1000, self.broadcast_public_key)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def set_encryption_method(self, method):
        self.encryption_method = method
        if method == "rsa":
            self.rsa_public_key, self.rsa_private_key = generate_rsa_keys(bit_length=2048)
        elif method == "elgamal":
            self.elgamal_public_key, self.elgamal_private_key = generate_elgamal_keys(7919)
        self.broadcast_public_key()
        messagebox.showinfo("Encryption Method", f"Encryption method set to {method.upper()}")

    def broadcast_public_key(self):
        try:
            if self.encryption_method == "rsa":
                key_message = f"PUBLIC_KEY:{self.client_name}:{self.encryption_method}:{self.rsa_public_key[0]}:{self.rsa_public_key[1]}"
            
            else:
                return
            print(f"DEBUG: Broadcasting public key: {key_message}")
            self.client_socket.send(key_message.encode())
        except Exception as e:
            print(f"DEBUG: Error broadcasting public key: {str(e)}")

    def encrypt_message(self, message, recipient=None):
        try:
            if recipient and recipient not in self.public_keys:
                print(f"DEBUG: No public key found for {recipient}")
                print(f"DEBUG: Available public keys: {list(self.public_keys.keys())}")
                return "ENCRYPTION_ERROR"
                
            if self.encryption_method == "hill":
                encrypted = hill_encrypt(message, self.hill_key)
                return base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')
            elif self.encryption_method == "rsa":
                if recipient:
                    recipient_key = self.public_keys[recipient]
                    print(f"DEBUG: Using public key for {recipient}: {recipient_key}")
                else:
                    recipient_key = self.rsa_public_key
                encrypted = rsa_encrypt_string(recipient_key, message)
                return base64.b64encode(str(encrypted).encode('utf-8')).decode('utf-8')
            
        except Exception as e:
            print(f"DEBUG: Encryption error: {str(e)}")
            return "ENCRYPTION_ERROR"

    def decrypt_message(self, encrypted_message):
        try:
            decoded = base64.b64decode(encrypted_message.encode('utf-8'))
            if self.encryption_method == "hill":
                return hill_decrypt(decoded.decode('utf-8'), self.hill_key)
            elif self.encryption_method == "rsa":
                ciphertext = int(decoded.decode('utf-8'))
                return rsa_decrypt_string(self.rsa_private_key, ciphertext)
           
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return "DECRYPTION_ERROR"

    def handle_public_key(self, message):
        try:
            parts = message.split(":")
            if len(parts) >= 5:
                _, sender, method = parts[:3]
                if method == "rsa" and len(parts) == 5:
                    e, n = map(int, parts[3:])
                    self.public_keys[sender] = (e, n)
                    print(f"DEBUG: Received RSA public key from {sender}")
                    print(f"DEBUG: Public key stored: {self.public_keys[sender]}")
               
                else:
                    print(f"DEBUG: Invalid public key format: {message}")
            else:
                print(f"DEBUG: Invalid public key format: {message}")
        except Exception as e:
            print(f"DEBUG: Error handling public key: {str(e)}")
            print(f"DEBUG: Message was: {message}")

    def on_listbox_select(self, event):
        selected_indices = self.client_listbox.curselection()
        self.current_selection = {self.client_listbox.get(i) for i in selected_indices}
        print(f"Current Selection: {self.current_selection}")

    def send_message(self):
        message = self.msg_entry.get()
        if message:
            try:
                if self.current_selection:
                    for client in self.current_selection:
                        encrypted_message = self.encrypt_message(message, client)
                        if encrypted_message == "ENCRYPTION_ERROR":
                            messagebox.showerror("Error", f"Failed to encrypt message for {client}")
                            continue
                        self.client_socket.send(f"PRIVATE {client} {self.encryption_method}:{encrypted_message}".encode())
                        self.display_message(f"You to {client} (Original): {message}", 'right')
                        self.display_message(f"You to {client} (Encrypted): {encrypted_message}", 'right')
                else:
                    encrypted_message = self.encrypt_message(message)
                    if encrypted_message == "ENCRYPTION_ERROR":
                        messagebox.showerror("Error", "Failed to encrypt message")
                        return
                    self.client_socket.send(f"BROADCAST {self.encryption_method}:{encrypted_message}".encode())
                    self.display_message(f"You (Broadcast) (Original): {message}", 'right')
                    self.display_message(f"You (Broadcast) (Encrypted): {encrypted_message}", 'right')

                self.msg_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")

    def show_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("Menu")

        tk.Button(menu, text="View Clients", command=self.view_clients).pack(pady=5)
        tk.Button(menu, text="Delete Client", command=self.delete_client).pack(pady=5)

    def view_clients(self):
        try:
            if self.client_socket:
                self.client_socket.send("REQUEST_CLIENT_LIST".encode())
            else:
                messagebox.showerror("Error", "Socket is not connected.")
        except OSError as e:
            messagebox.showerror("Error", f"Socket error: {e}")

    def delete_client(self):
        client_name = simpledialog.askstring("Delete Client", "Enter the client's name to delete:", parent=self.root)
        if client_name:
            try:
                if self.client_socket:
                    self.client_socket.send(f"DELETE_CLIENT {client_name}".encode())
                else:
                    messagebox.showerror("Error", "Socket is not connected.")
            except OSError as e:
                messagebox.showerror("Error", f"Socket error: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(4096).decode('utf-8', errors='ignore')  # Increased buffer size
                if not message:
                    break

                print(f"DEBUG: Received raw message: {message}")

                if message.startswith("PUBLIC_KEY"):
                    self.handle_public_key(message)
                    self.print_public_keys()  # Print current state of public keys
                elif message.startswith("CLIENT_LIST"):
                    self.show_client_list(message[len("CLIENT_LIST\n"):])
                    # Request public keys after receiving client list
                    self.broadcast_public_key()
                elif message.startswith("BROADCAST") or message.startswith("PRIVATE"):
                    self.handle_chat_message(message)
                else:
                    self.display_message(message, 'left')
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def handle_chat_message(self, message):
        parts = message.split(" ", 2)
        if len(parts) >= 3:
            msg_type, sender, content = parts
            encryption_method, encrypted_content = content.split(":", 1)
            if encryption_method != self.encryption_method:
                self.display_message(f"Cannot decrypt message from {sender}. Different encryption method used.", 'left')
            else:
                decrypted_content = self.decrypt_message(encrypted_content)
                if decrypted_content == "DECRYPTION_ERROR":
                    self.display_message(f"Error decrypting message from {sender}", 'left')
                else:
                    self.display_message(f"From {sender} (Encrypted): {encrypted_content}", 'left')
                    self.display_message(f"From {sender} (Decrypted): {decrypted_content}", 'left')
        else:
            self.display_message(f"Invalid message format: {message}", 'left')

    def show_client_list(self, client_list):
        self.client_list = client_list.split("\n")
        self.client_listbox.delete(0, tk.END)
        for client in self.client_list:
            self.client_listbox.insert(tk.END, client)

    def display_message(self, message, align):
        self.chat_window.configure(state=tk.NORMAL)
        tag = 'left' if align == 'left' else 'right'
        self.chat_window.tag_configure(tag, justify='left' if align == 'left' else 'right', foreground='black' if align == 'left' else 'blue')
        self.chat_window.insert(tk.END, f"{message}\n", tag)
        self.chat_window.configure(state=tk.DISABLED)
        self.chat_window.yview(tk.END)

    def print_public_keys(self):
        print("DEBUG: Current public keys:")
        for sender, key in self.public_keys.items():
            print(f"  {sender}: {key}")

def start_client():
    root = tk.Tk()

    server_ip = "127.0.0.1"
    server_port = 8082

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Unable to connect to the server.")
        return

    name = simpledialog.askstring("Name", "Enter your name:", parent=root)
    if not name:
        return

    client_socket.send(name.encode())

    app = ClientApp(root, client_socket, name)
    root.mainloop()

if __name__ == "__main__":
    start_client()

