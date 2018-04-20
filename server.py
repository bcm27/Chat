#!/usr/bin/env python3
import re
import util.server.serverUtils as sUtils
from socket import *
from threading import Thread
from util.server.dbMethods import DBMethods
from util.sharedUtils import SERVER_PORT
import time

CONNECTED_CLIENTS = []
MAX_CLIENTS = 10
arrayOfStoredMessages = []


class messageObject:
    def __init__(self, sender, recipient, message):
        self.sender = sender
        self.recipient = recipient
        self.message = message

    def getSender(self):
        return self.sender

    def getRecipient(self):
        return self.recipient

    def getMessage(self):
        return self.message


def main():
    global server_socket  # Must be "global" to close in `finally` statement

    try:
        sUtils.cls()  # Clear the screen
        print('Starting ChatApp Server')  # Notify that we're starting the server

        server_socket = socket(AF_INET, SOCK_STREAM)  # Set up the TCP server
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Reuse a port number immediately after socket closes
        server_socket.bind(("", SERVER_PORT))  # Bind to localhost:SERVER_PORT
        server_socket.listen(MAX_CLIENTS)  # Accept maximum of 10 clients

        while True:
            print("Waiting for " + ("a" if len(CONNECTED_CLIENTS) < 1 else "another") + " connection...")

            client_socket = None
            try:
                client_socket, client_address = server_socket.accept()  # Wait to accept an incoming client connection
                Thread(target=listenToClient, args=[client_socket, client_address]).start()  # Start a new listening thread

            except KeyboardInterrupt:
                if client_socket:
                    client_socket.close()
                break
            print("Connection acquired: {0}".format(str(client_address)))  # Notify a connection was made

    except KeyboardInterrupt:
        pass
    except Exception as e:
        sUtils.cls()  # Clear the screen
        print(e)  # Print the error
        exit(-1)  # Close
    finally:
        sUtils.cls()  # Clear the screen
        server_socket.close()  # Close the server socket
        print('PythonChat Server cleanup and exit...done!')
        exit(0)  # Close


def listenToClient(client_socket, client_address):
    while 1:
        try:
            data = client_socket.recv(1024)

            if data is not None:
                request = re.split(" +", data.decode())

                if request is not None:

                    def get_jwt(req):
                        if req[0] == '/login':  # `/login username hashed_pass_here`
                            return DBMethods.login(req[1], req[2])

                        elif req[0] == '/register':  # `/register username hashed_pass_here`
                            if DBMethods.register(req[1], req[2]):
                                return DBMethods.login(req[1], req[2])

                        elif req[0] == '/verify':  # `/verify jwt.code.here`
                            if sUtils.decodeJWT(req[1]) is not None:
                                return req[1]

                    jwt = get_jwt(request)

                    if jwt is not None:
                        if jwt == "<FAILED LOGIN ATTEMPTS>":
                            client_socket.send(bytes("<FAILED LOGIN ATTEMPTS>", "UTF-8"))
                            client_socket.close()

                        decoded_jwt = sUtils.decodeJWT(jwt)

                        username = decoded_jwt.get('username')  # Get the username from the JWT payload
                        client_dic = {username: client_socket}  # Dictionary of `key:username` and `value:socket`

                        CONNECTED_CLIENTS.append(
                            client_dic)  # Add the client dictionary to the list of connected client
                        client_socket.send(bytes("<ACCEPTED>", "UTF-8"))
                        sendUserLists()

                        for x in arrayOfStoredMessages:
                            if x.getRecipient() == username:
                                client_socket.send(bytes("/message " + x.getMessage(), "UTF-8"))
                                # remove the message from the backlog
                                arrayOfStoredMessages.remove(x)

                        while True:  # While there's no errors
                            try:
                                data = client_socket.recv(1024)  # Wait for incoming data from client
                                if data:  # If there's data...
                                    # Do requested action from client
                                    decoded = data.decode()
                                    request = re.split(" +", decoded)

                                    if request[0] == '/message' or request[0] == '/private':
                                        hasSent = False
                                        for client_dict in CONNECTED_CLIENTS:
                                            for dict_username, dict_socket in client_dict.items():
                                                if dict_username == request[1]:
                                                    hasSent = True
                                                    dict_socket.send(
                                                        bytes(("Message from " + username + ": " + decoded),"UTF-8"))
                                        if not hasSent:
                                            storedMessage = messageObject(sender=username, recipient=request[1],
                                                                          message=" ".join(request).split(" ", 1)[1])
                                            arrayOfStoredMessages.append(storedMessage)
                                            print("storedMessage: " + storedMessage.getMessage())

                                    elif request[0] == '/something':
                                        dict_socket.send(bytes("I did something", "UTF-8"))
                                    else:
                                        for client_dict in CONNECTED_CLIENTS:
                                            for dict_username, dict_socket in client_dict.items():
                                                dict_socket.send(bytes((username + ": " + decoded), "UTF-8"))

                                else:  # No data, client must've disconnected
                                    raise error()  # Throw an error to exit while loop
                            except Exception as e_:
                                print("Client disconnected:", e_)
                                CONNECTED_CLIENTS.remove(client_dic)
                                client_socket.close()
                                sendUserLists()
                                return False
                    else:
                        client_socket.send(bytes("<DECLINED>", "UTF-8"))
                else:
                    client_socket.send(bytes("<DECLINED>", "UTF-8"))
            else:
                print("Client disconnected")
                client_socket.close()
                return False

        except Exception as e:
            print(e)
            print("Client disconnected")
            client_socket.close()
            return False


def sendUserLists():
    usernameList = []
    for client_dict in CONNECTED_CLIENTS:
        for dict_username, dict_socket in client_dict.items():
            usernameList.append(dict_username)
    for client_dict in CONNECTED_CLIENTS:
        for dict_username, dict_socket in client_dict.items():
            dict_socket.send(bytes(("/userlist " + " ".join(usernameList)), "UTF-8"))


if __name__ == '__main__':
    main()
