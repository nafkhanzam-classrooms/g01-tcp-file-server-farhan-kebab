import socket
import select
import os

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

sockets = [server]

os.makedirs("server_files", exist_ok=True)

print("Select Server running...")

while True:

    read_sockets, _, _ = select.select(sockets, [], [])

    for sock in read_sockets:

        if sock == server:
            conn, addr = server.accept()
            sockets.append(conn)
            print("Connected", addr)

        else:
            data = sock.recv(4096)

            if not data:
                sockets.remove(sock)
                sock.close()
                continue

            msg = data.decode()

            if msg.startswith("/list"):
                files = os.listdir("server_files")
                sock.send(str(files).encode())

            else:
                for s in sockets:
                    if s != server and s != sock:
                        s.send(data)