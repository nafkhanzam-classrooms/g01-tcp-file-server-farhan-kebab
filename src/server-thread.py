import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 5000

clients = []

os.makedirs("server_files", exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Thread Server running...")


def broadcast(msg, conn):
    for c in clients:
        if c != conn:
            c.send(msg)


def handle(conn, addr):
    print("Connected", addr)

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break

            if data.startswith("/list"):
                files = os.listdir("server_files")
                conn.send(str(files).encode())

            elif data.startswith("/upload"):
                filename = data.split()[1]

                with open("server_files/" + filename, "wb") as f:
                    chunk = conn.recv(4096)
                    while chunk != b"EOF":
                        f.write(chunk)
                        chunk = conn.recv(4096)

            elif data.startswith("/download"):
                filename = data.split()[1]
                path = "server_files/" + filename

                if os.path.exists(path):
                    conn.send(f"FILE {filename}".encode())

                    with open(path, "rb") as f:
                        chunk = f.read(4096)
                        while chunk:
                            conn.send(chunk)
                            chunk = f.read(4096)

                    conn.send(b"EOF")

            else:
                broadcast(data.encode(), conn)

        except:
            break

    clients.remove(conn)
    conn.close()


while True:
    conn, addr = server.accept()
    clients.append(conn)

    thread = threading.Thread(target=handle, args=(conn, addr))
    thread.start()