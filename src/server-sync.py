import socket
import os

HOST = "0.0.0.0"
PORT = 5000

os.makedirs("server_files", exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server Sync running...")

while True:
    conn, addr = server.accept()
    print("Connected:", addr)

    while True:
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
                    data = f.read(4096)
                    while data:
                        conn.send(data)
                        data = f.read(4096)

                conn.send(b"EOF")
            else:
                conn.send(b"File not found")

    conn.close()