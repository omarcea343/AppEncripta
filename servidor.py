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
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                for c in self.connections:
                    if c != conn:
                        c.sendall(data)
            except Exception as e:
                print(f"Error al manejar el cliente: {e}")
                self.connections.remove(conn)
                conn.close()
                break

if __name__ == "__main__":
    servidor = Servidor()
    servidor.start()
