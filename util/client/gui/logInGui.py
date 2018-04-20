import util.client.clientUtils as cUtils
from tkinter import *
from util.client.gui import gui

import socket
from sys import argv
from util.sharedUtils import SERVER_PORT
import time

class LoginGUI:
    def __init__(self, client_socket):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket
        client_socket.connect((argv[1] if len(argv) > 1 else "localhost", SERVER_PORT))  # Connect to the socket
        window = Tk()

        window.resizable(0, 0)
        window.title("Welcome to Python Chat!")

        canvasBottom = Canvas(window, width=400, height=50)
        canvasTop = Canvas(window, width=400, height=50)

        label_one = Label(window, text='User:')
        label_two = Label(window, text='Password:')

        user_name_text_field = Entry(window, textvariable=StringVar())
        password_text_field = Entry(window, show='*', textvariable=StringVar())

        def display_toast(message):
            label_message = Label(window, text=message)
            label_message.pack()

            def clear_label():
                label_message.destroy()

            label_message.after(2000, clear_label)  # Clear label after 2 seconds

        def login_or_register(should_login):
            user = user_name_text_field.get()
            password = password_text_field.get()

            if not user or not password:
                display_toast('Please fill in all required fields!')
            else:
                server_login_cb(client_socket, should_login, user, password, window, display_toast)

        def login_on_click():
            login_or_register(True)

        def register_on_click():
            login_or_register(False)

        login_button = Button(window, text='Log In', command=login_on_click)
        register_button = Button(window, text='Register', command=register_on_click)

        label_login = Label(window, text='Login Now or Register', fg="orange red", font=("Georgia", 16, "bold"))
        label_welcome = Label(window, text='Welcome to Python Chat!', fg="deep sky blue", font=("Georgia", 18, "bold "))
        canvasTop.pack()
        label_welcome.pack()
        label_login.pack()

        blueBox = canvasTop.create_rectangle(0, 0, 400, 30, fill="deep sky blue")

        label_one.pack()
        user_name_text_field.pack()
        label_two.pack()
        password_text_field.pack()

        login_button.pack()
        register_button.pack()

        blueBox = canvasBottom.create_rectangle(0, 50, 400, 30, fill="deep sky blue", )

        canvasBottom.pack()

        window.mainloop()


def server_login_cb(client_socket, should_login, p_user, p_pass, login_ui_window, display_toast):

    if should_login:
        log_attempt = cUtils.send_login_command(client_socket, p_user, p_pass)
        print("Login Status: %s" % log_attempt)
        if log_attempt == "<ACCEPTED>":
            login_ui_window.withdraw()
            gui.start_gui(client_socket)  # Start the main GUI and pass it the created socket
        if log_attempt == "<FAILED LOGIN ATTEMPTS>":
            display_toast("Too many invalid login attempts...closing")
            time.sleep(2)
            display_toast("Closing...")
            time.sleep(3)
            client_socket.close()
            sys.exit(-1)
        else:
            display_toast("Invalid username or password.")
    else:
        if cUtils.send_register_command(client_socket, p_user, p_pass):
            login_ui_window.withdraw()
            gui.start_gui(client_socket)  # Start the main GUI and pass it the created socket
        else:
            display_toast("That username is already in use.")
