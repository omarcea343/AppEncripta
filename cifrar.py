import tkinter as tk
from tkinter import ttk
import algoritmo
import socket

class CifrarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cifrar App")
        self.master.geometry("820x720")
        self.master.config(padx=10, pady=10)

        # Apply Clam theme
        style = ttk.Style()
        style.theme_use('clam')

        # Create the encryption object
        self.encryption = algoritmo

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

        self.message_label = ttk.Label(self.left_panel, text="Mensaje:")
        self.message_label.pack()

        self.message_entry = tk.Text(self.left_panel, height=10)
        self.message_entry.pack(fill=tk.BOTH, expand=True)

        self.encrypt_button = ttk.Button(self.left_panel, text="Encriptar", command=self.encrypt_message)
        self.encrypt_button.pack()

        self.send_button = ttk.Button(self.left_panel, text="Enviar", command=self.send_message)
        self.send_button.pack()

        # Right panel for output
        self.right_panel = ttk.Frame(self.main_panel, width=500, height=600)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.right_panel.pack_propagate(0)

        self.encrypted_message_label = ttk.Label(self.right_panel, text="Mensaje encriptado:")
        self.encrypted_message_label.pack()

        self.encrypted_message_text = tk.Text(self.right_panel, height=10)
        self.encrypted_message_text.pack(fill=tk.BOTH, expand=True)

        self.key_label = ttk.Label(self.right_panel, text="Clave hash:")
        self.key_label.pack()

        self.key_text = tk.Text(self.right_panel, height=5)
        self.key_text.pack(fill=tk.BOTH, expand=True)

        self.steps_label = ttk.Label(self.right_panel, text="Pasos:")
        self.steps_label.pack()

        # Add a scrollbar to the steps_text widget
        self.steps_scrollbar = ttk.Scrollbar(self.right_panel)
        self.steps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.steps_text = tk.Text(self.right_panel, height=15, yscrollcommand=self.steps_scrollbar.set)
        self.steps_text.pack(fill=tk.BOTH, expand=True)

        self.steps_scrollbar.config(command=self.steps_text.yview)


    def encrypt_message(self):
        try:
            message = self.message_entry.get("1.0", tk.END).encode()
            encrypted_message, key, steps = self.encryption.encrypt_message(message)
            self.encrypted_message_text.delete("1.0", tk.END)
            self.encrypted_message_text.insert(tk.END, encrypted_message.hex())
            self.key_text.delete("1.0", tk.END)
            self.key_text.insert(tk.END, key.hex())
            self.steps_text.delete("1.0", tk.END)
            self.steps_text.insert(tk.END, "\n".join(steps))
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while encrypting the message: {e}")

    def send_message(self):
        # Get the encrypted message and key
        encrypted_message = self.encrypted_message_text.get("1.0", tk.END).strip()
        key = self.key_text.get("1.0", tk.END).strip()

        # Create a socket and connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 1234))

        # Send the encrypted message and key to the server
        s.sendall(f"{encrypted_message}\n{key}".encode())

        # Close the socket
        s.close()



if __name__ == "__main__":
    root = tk.Tk()
    app = CifrarApp(root)
    root.mainloop()
