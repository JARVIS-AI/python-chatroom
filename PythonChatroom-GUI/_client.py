# Import libraries for network communication
import socket
import threading

# Create a socket object for network communication
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

counter = 0


async def new_user(_username: str = None, _host: str = None, _port: int = None):
    """
    This asynchronous function establishes a connection with the chat server
    and performs initial setup for a new user.

    Args:
        _username (str, optional): The desired username. Defaults to None,
            in which case a default username is generated.
        _host (str, optional): The hostname or IP address of the chat server.
            Defaults to the local machine's hostname.
        _port (int, optional): The port number of the chat server. Defaults to 1234.

    Returns:
        tuple[str, str]: A tuple containing two elements:
            * The welcome message received from the server.
            * The server's response message after sending the username.
    """
    global counter
    global socket_server

    # Determine server connection details
    server_host = socket.gethostname() if _host is None else _host
    server_port = 9999 if _port is None else _port

    # Connect to the chat server
    socket_server.connect((server_host, server_port))

    # Receive the welcome message from the server
    welcome_message = socket_server.recv(1024).decode()

    # Generate a unique username if none provided
    if _username is None:
        _username = f"user_{counter}"
    counter += 1

    # Send the username to the server
    socket_server.send(_username.encode())

    # Receive the server's response message after sending the username
    _message = socket_server.recv(1024).decode()

    return welcome_message, _message


async def exit_server(sock: socket.socket, msg: str = "QUIT") -> bool:
    """
    Gracefully disconnects the user from the chat server.

    This function sends a message (defaulting to "QUIT") to the server
    indicating the user's intent to exit. It then optionally closes the socket
    connection if the message sent is "QUIT".

    Args:
        sock (socket.socket): The socket object used for communication with the server.
        msg (str, optional): The message to send to the server on exit. Defaults to "QUIT".

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    try:
        # Send exit message to server
        sock.send(msg.encode())

        # Close socket connection if message is "QUIT"
        if msg == "QUIT":
            sock.close()

        return True
    except:
        # Handle potential exceptions during message sending
        return False


async def send_message_to_server(sock: socket.socket, msg: str) -> bool:
    """
    Sends a message to the chat server over the provided socket connection.

    This function attempts to send the provided message (`msg`) to the server.
    On successful transmission, it returns True. Otherwise, it returns False
    indicating an error during message sending.

    Args:
        sock (socket.socket): The socket object representing the connection to the server.
        msg (str): The message content to be sent to the server.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    try:
        # Attempt to send message over the socket
        sock.send(msg.encode())
        return True
    except:
        # Handle exceptions during message sending
        return False
