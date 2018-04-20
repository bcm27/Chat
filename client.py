import socket
from sys import argv
from util.client.gui.logInGui import LoginGUI
from util.sharedUtils import SERVER_PORT


def main():
    print('Starting ChatApp Client')  # Announce the client is starting

    # starts the client process
    LoginGUI((argv[1] if len(argv) > 1 else "localhost", SERVER_PORT))


if __name__ == '__main__':
    main()
