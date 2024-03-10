import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 9001

server.connect((host, port))

message = server.recv(1024)
print(message.decode())

name = input("\033[35mEnter Your Username: ")
print("\033[0m")
server.send(name.encode())

message = server.recv(1024)
print(message.decode())

def get_new_msg(sock):
    global quit
    quit = False
    while not quit:
        try:
            msg = sock.recv(1024)
            print("\033[37m", end="")
            print(msg.decode(), end="")
            print("\033[0m", end="")
        except:
            break

t = threading.Thread(target=get_new_msg, args=(server,))
t.daemon = True
t.start()

while True:
    print("\033[37m", end="")
    message = input(str("You : "))
    print("\033[0m", end="")

    server.send(message.encode())

    if message == "!q":
        server.close()
        break

print("\033[32mHave Good Day ...!\033[0m")
