import socket
import threading

class Servidor:
    def __init__(self):
        self.host = "localhost"
        self.port = 1234
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.connections = []

    def start(self):
        print(f"Servidor iniciado en {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            print(f"Conexión establecida desde {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

import socket
import threading

class Servidor:
    def __init__(self):
        self.host = "localhost"
        self.port = 1234
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.connections = []

    def start(self):
        print(f"Servidor iniciado en {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            print(f"Conexión establecida desde {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        try:
            # Receive the message and key from the client
            message_and_key = conn.recv(1024).decode()

            # Split the message and key using the '|' separator
            encrypted_message, key = message_and_key.split("|")

            # Print the message and key received from the client
            print(f"Mensaje recibido: {encrypted_message}")
            print(f"Clave recibida: {key}")

            # Send the encrypted message and key to all other clients
            for c in self.connections:
                if c != conn:
                    # Combine the encrypted message and key into a single string, separated by '|'
                    message_and_key = f"{encrypted_message}|{key}"
                    c.sendall(message_and_key.encode())
        except Exception as e:
            print(f"Error al manejar el cliente: {e}")
        finally:
            self.connections.remove(conn)
            conn.close()

if __name__ == "__main__":
    servidor = Servidor()
    servidor.start()



if __name__ == "__main__":
    servidor = Servidor()
    servidor.start()
