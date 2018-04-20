import os
import tkinter
import tkinter.ttk as ttk
from threading import Thread
from tkinter import *
import socket
from sys import argv
from util.sharedUtils import SERVER_PORT


def start_gui(client_socket):
    """Starting point when module is the main routine.
    :param client_socket: The socket created by the client - used to send messages on click
    """

    root = Tk()
    root.resizable(False, False)

    def on_closing():
        client_socket.close()  # Close the socket
        root.destroy()  # Close the GUI
        sys.exit(1)  # Stop the process

    root.protocol("WM_DELETE_WINDOW", on_closing)  # On window closing, do on_closing
    GuiFrame(client_socket, root).start()
    root.mainloop()


class GuiFrame(Thread):

    def __init__(self, client_socket, root_frame=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window.
           :param client_socket: """
        super().__init__()
        self.client_socket = client_socket
        self.root = root_frame

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        root_frame.geometry("600x450")
        root_frame.title("ChatApp")
        root_frame.configure(background="#b9f9c8")
        root_frame.configure(highlightbackground="#d9d9d9")
        root_frame.configure(highlightcolor="black")

        self.Scrolledlistbox1 = ScrolledListBox(root_frame)
        self.Scrolledlistbox1.place(relx=0.577, rely=0.0, relheight=1.0, relwidth=0.42)
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox1.configure(font="TkFixedFont")
        self.Scrolledlistbox1.configure(foreground="black")
        self.Scrolledlistbox1.configure(highlightbackground="#b9fcb6")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#b1f88f")
        self.Scrolledlistbox1.configure(selectforeground="black")
        self.Scrolledlistbox1.configure(width=10)

        self.Text1 = Text(root_frame)
        self.Text1.place(relx=0.004, rely=0.004, relheight=0.9, relwidth=0.57)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(width=349)
        self.Text1.configure(wrap=WORD)

        self.Entry1 = Entry(root_frame)
        self.Entry1.place(relx=0.003, rely=0.91, relheight=0.084, relwidth=0.457)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(width=194)

        def send_message_to_server():
            message = self.Entry1.get()
            if len(message) > 0:
                self.Entry1.delete(0, 'end')
                client_socket.send(bytes(message, 'UTF-8'))
                self.Text1.see(tkinter.END)

        self.Entry1.bind("<Return>", (lambda event: send_message_to_server()))

        self.Button1 = Button(root_frame, command=send_message_to_server)
        self.Button1.place(relx=0.464, rely=0.908, height=39, width=67)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Send''')
        self.Entry1.focus()

    def run(self):
        """
        This is an internal class thread, which is tkinter thread-safe
        """
        while 1:
            try:
                data = self.client_socket.recv(1024)
                if not data:  # Socket has closed
                    break

                data = data.decode('UTF-8')

                request = re.findall(r"[^\/]+", data)
                for commandStr in request:
                    command = commandStr.split(' ', 1)[0]

                    if command == "userlist": # `/userlist username1 username2 username3...
                        userList = []

                        for idx, val in enumerate(commandStr.split(" ", 1)[1].split(" ")):
                            userList.append(val)

                        if len(userList) > 0:
                            self.Scrolledlistbox1.delete(0, END)
                            for user in userList:
                                self.Scrolledlistbox1.insert(0, user)

                    elif command == "message":
                        username = commandStr[2]
                        #message = commandStr.split(" ")
                        #print(message)
                        #self.Text1.insert(END, "Message from " + username + " : " + message + "\n")
                        self.Text1.insert(END, "Message from " + username + " :" + commandStr.split(" ", 2)[2] + "\n")
                    else:
                        self.Text1.insert(END, data + "\n")

            except Exception as e:
                print(e)
                break

        #self.Text1.insert(END, "Disconnected from the server.\n")  # Uncomment if you don't want GUI to close
        #os._exit(1)


class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        methods = Pack.__dict__.keys() | Grid.__dict__.keys() | Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped


def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)

    return wrapped


class ScrolledListBox(AutoScroll, Listbox):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
