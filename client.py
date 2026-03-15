import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive():
    while True:
        try:
            msg = client.recv(4096).decode()
            if msg.startswith("FILE "):
                filename = msg.split()[1]
                with open("download_" + filename, "wb") as f:
                    data = client.recv(4096)
                    while data != b"EOF":
                        f.write(data)
                        data = client.recv(4096)
                print("Downloaded", filename)
            else:
                print(msg)
        except:
            break


def send():
    while True:
        msg = input()

        if msg.startswith("/upload"):
            filename = msg.split()[1]
            client.send(msg.encode())

            with open(filename, "rb") as f:
                data = f.read(4096)
                while data:
                    client.send(data)
                    data = f.read(4096)

            client.send(b"EOF")

        else:
            client.send(msg.encode())


threading.Thread(target=receive).start()
threading.Thread(target=send).start()