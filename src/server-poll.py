import socket
import select

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

poll = select.poll()
poll.register(server, select.POLLIN)

fd_to_socket = {server.fileno(): server}

print("Poll Server running...")

while True:

    events = poll.poll()

    for fd, flag in events:

        sock = fd_to_socket[fd]

        if sock == server:
            conn, addr = server.accept()
            print("Connected", addr)

            fd_to_socket[conn.fileno()] = conn
            poll.register(conn, select.POLLIN)

        else:
            data = sock.recv(4096)

            if not data:
                poll.unregister(fd)
                sock.close()
                del fd_to_socket[fd]

            else:
                for s in fd_to_socket.values():
                    if s != server and s != sock:
                        s.send(data)