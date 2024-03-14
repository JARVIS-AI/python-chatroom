import socket
import threading

from models import SavedMessage

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 9999
s.bind((host, port))

s.listen(5)
print(f"\033[32mserver listening on {host} ({socket.gethostbyname(host)})\033[0m")

clients = []


def broadcast(message, cli=None, name=None):
    """
    Broadcasts a message to all connected clients, excluding the sender if specified.
    Also saves the message to the database for persistence.

    Args:
        message (bytes): The message to be broadcast, encoded as bytes.
        cli (optional): The client object representing the sender, if applicable.
                       Used to exclude the sender from receiving the message.
        name (optional): The username associated with the message, for saving and broadcasting.
    """
    # Iterate through connected clients and broadcast, excluding sender:
    for c, client_name in clients:
        # Skip sender if specified
        if c == cli:
            continue
        else:
            # Send message to client
            c.send(message)

    # Store message persistently in the database:
    SavedMessage(username=name, content=message.decode().replace(f"{name}: ", "")).save()

def handle_client(c, addr):
    c.send("welcome to chat rome".encode())

    try:
        name = c.recv(1024).decode()
    except:
        print(f"\033[31mclient {addr} disconnected ...!\033[0m")
        return c.close()

    print(f"\033[33mclient {addr} - username :  \033[35m{name}\033[33m ...!\033[0m")

    c.send(f"Hi {name}. Enter QUIT for Exit.".encode())

    broadcast(f"{name} ENTERED to chat room".encode(), c, name)

    clients.append((c, name))

    while True:
        try:
            message = c.recv(1024)
            if message == b"QUIT":
                print(f"\033[33mclient {addr} - username :  \033[35m{name}\033[33m disconnected ...!\033[0m")
                clients.remove((c, name))
                broadcast(f"{name} LEFT The Chat Room".encode(),cli=None, name=name)
                return c.close()
            else:
                broadcast(f"{name}: {message.decode()}".encode(), c, name)
        except:
            print(f"\033[33mclient {addr} - username :  \033[35m{name}\033[33m disconnected ...!\033[0m")
            clients.remove((c, name))
            broadcast(f"{name} LEFT The Chat Room".encode(),cli=None, name=name)
            return c.close()


while True:
    c, addr = s.accept()
    print(f"\034[33mclient {addr} connected ...!\033[0m")

    t = threading.Thread(target=handle_client, args=(c, addr))
    t.start()
