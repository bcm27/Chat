import socket
from sys import argv
from util.client.gui.logInGui import LoginGUI
from util.sharedUtils import SERVER_PORT


def main():
    print('Starting ChatApp Client')  # Announce the client is starting

    # below have been moved into LoginGUI()
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket
    #client_socket.connect((argv[1] if len(argv) > 1 else "localhost", SERVER_PORT))  # Connect to the socket

    LoginGUI()


if __name__ == '__main__':
    main()
