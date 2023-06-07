import socket
import threading

class Servidor:
    def __init__(self):
        self.host = "25.66.163.155"
        self.port = 58765
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

    def handle_client(self, conn, client_socket=None):
        try:
            # Receive the message and key from the client
            message_and_key = conn.recv(1024).decode()

            # Check if the message is a request for data
            if message_and_key == "request_data":
                # Send the encrypted message and key to the requesting client
                conn.sendall(f"{self.encrypted_message}|{self.key}".encode())
            else:
                # Split the message and key using the '|' separator
                encrypted_message, key = message_and_key.split("|")

                # Print the message and key received from the client
                print(f"Mensaje recibido: {encrypted_message}")
                print(f"Clave recibida: {key}")

                # Save the encrypted message and key for future requests
                self.encrypted_message = encrypted_message
                self.key = key

                # Send the encrypted message and key to all connected clients except the sender
                for c in self.connections:
                    if c != conn:
                        # Send the encrypted message
                        c.sendall(encrypted_message.encode())
                        # Wait for the client to acknowledge the message
                        c.recv(1024)
                        # Send the key
                        c.sendall(key.encode())

        except Exception as e:
            print(f"Error al manejar el cliente: {e}")
        finally:
            self.connections.remove(conn)
            conn.close()


if __name__ == "__main__":
    servidor = Servidor()
    servidor.start()
