import tkinter as tk
from tkinter import ttk
import algoritmo
import socket
from tkinter import messagebox

class DesencriptarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Desencriptar App")
        self.master.geometry("820x720")
        self.master.config(padx=10, pady=10)

        # Apply Clam theme
        style = ttk.Style()
        style.theme_use('clam')

        # Create the decryption object
        self.decryption = algoritmo

        # Create the GUI
        self.create_gui()

    def create_gui(self):
        # Create the menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # Create the File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Main panel for left and right panels
        self.main_panel = ttk.Frame(self.master, width=700, height=600)
        self.main_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left panel for message input
        self.left_panel = ttk.Frame(self.main_panel, width=200, height=600)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_panel.pack_propagate(0)

        self.receive_button = ttk.Button(self.left_panel, text="Recibir datos del servidor", command=self.receive_data)
        self.receive_button.pack()
        
        self.message_label = ttk.Label(self.left_panel, text="Mensaje encriptado:")
        self.message_label.pack()

        self.message_entry = tk.Text(self.left_panel, height=10)
        self.message_entry.pack(fill=tk.BOTH, expand=True)

        self.key_label = ttk.Label(self.left_panel, text="Clave hash:")
        self.key_label.pack()

        self.key_entry = tk.Text(self.left_panel, height=5)
        self.key_entry.pack(fill=tk.BOTH, expand=True)

        self.decrypt_button = ttk.Button(self.left_panel, text="Desencriptar", command=self.decrypt_message)
        self.decrypt_button.pack()

        # Right panel for output
        self.right_panel = ttk.Frame(self.main_panel, width=500, height=600)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.right_panel.pack_propagate(0)

        self.decrypted_message_label = ttk.Label(self.right_panel, text="Mensaje desencriptado:")
        self.decrypted_message_label.pack()

        self.decrypted_message_text = tk.Text(self.right_panel, height=10)
        self.decrypted_message_text.pack(fill=tk.BOTH, expand=True)

        self.steps_label = ttk.Label(self.right_panel, text="Pasos:")
        self.steps_label.pack()

        # Add a scrollbar to the steps_text widget
        self.steps_scrollbar = ttk.Scrollbar(self.right_panel)
        self.steps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.steps_text = tk.Text(self.right_panel, height=15, yscrollcommand=self.steps_scrollbar.set)
        self.steps_text.pack(fill=tk.BOTH, expand=True)

        self.steps_scrollbar.config(command=self.steps_text.yview)

    def receive_data(self):
        try:
            # Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("localhost", 58765))

            # Send a request for data
            client_socket.sendall(b"request_data")

            # Receive the data from the server
            data = client_socket.recv(1024).decode()

            # Split the data into the encrypted message and key
            encrypted_message, key = data.split("|")

            # Show the encrypted message and key in the GUI
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.insert(tk.END, encrypted_message)
            self.key_entry.delete("1.0", tk.END)
            self.key_entry.insert(tk.END, key)
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while receiving data from the server: {e}")
        finally:
            client_socket.close()
    
    def decrypt_message(self):
        try:
            if self.message_entry.get("1.0", tk.END).strip() == "" and self.key_entry.get("1.0", tk.END).strip() == "":
                # If there is no data entered manually, try to receive data from the server
                self.receive_data()

            encrypted_message = bytes.fromhex(self.message_entry.get("1.0", tk.END).strip())
            key = bytes.fromhex(self.key_entry.get("1.0", tk.END).strip())
            decrypted_message, steps = self.decryption.decrypt_message(encrypted_message, key)
            self.decrypted_message_text.delete("1.0", tk.END)
            self.decrypted_message_text.insert(tk.END, decrypted_message.decode())
            self.steps_text.delete("1.0", tk.END)
            for step in steps:
                self.steps_text.insert(tk.END, step + "\n")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while decrypting the message: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesencriptarApp(root)
    root.mainloop()
