import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 1234
server.bind((host, port))

server.listen(5)
print(f"\033[32mserver listening on {host} ({socket.gethostbyname(HOST)})\033[0m")

clients = []


def broadcast(message, cli=None):
    for c, name in clients:
        if c == cli:
            continue
        else:
            c.send(message)


def handle_client(c, addr):
    c.send("\r\033[36m\t\t\twelcome to chat rome\033[0m".encode())

    try:
        name = c.recv(1024).decode()
    except:
        print(f"\033[31mclient {addr} disconnected ...!\033[0m")
        return c.close()

    print(f"\033[33mclient {addr} - username :  \033[35m{name}\033[33m ...!\033[0m")

    c.send(f"\r\033[32mHi {name}. Enter QUIT for Exit.\033[0m".encode())

    broadcast(f"\r\033[36m{name} Entered to chat room\n\033[37mYou : \033[0m".encode(), c)

    clients.append((c, name))

    while True:
        try:
            message = c.recv(1024)
            if message == b"!q":
                print(f"\033[33mclient {addr} - username :  \033[35m{name}\033[33m disconnected ...!\033[0m")
                clients.remove((c, name))
                broadcast(f"\r\033[31m{name} Left The Chat Room\n\033[37mYou : ".encode())
                return c.close()
            else:
                broadcast(f"\r\033[36m{name}: {message.decode()}\n\033[37mYou : ".encode(), c)
        except:
            print(f"\033[33mclient {addr} - username :  \033[35m{name}\033[33m disconnected ...!\033[0m")
            clients.remove((c, name))
            broadcast(f"\r\033[31m{name} Left The Chat Room\n\033[37mYou : ".encode())
            return c.close()


while True:
    c, addr = server.accept()
    print(f"\033[33mclient {addr} connected ...!\033[0m")

    t = threading.Thread(target=handle_client, args=(c, addr))
    t.start()
