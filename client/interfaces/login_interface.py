from protocol.protocol import MessageType, packet
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import client.mem
from utils import get_config
from client.interfaces.main_interface import MainInterface

config = get_config()

class LoginInterface(tk.Frame):
    def __init__(self, client, master=None):
        super().__init__(master)
        self.master = master
        self.client = client
        self.createForm()
        master.protocol("WM_DELETE_WINDOW", self.destroy_window)

    def createForm(self):
        self.master.resizable(width=False, height=False)
        self.master.geometry('300x100')        
        self.master.title("Book Reader")

        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")

        self.username = Entry(self)
        self.password = Entry(self, show="*")

        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)

        self.username.grid(row=0, column=1, pady=(10, 6))
        self.password.grid(row=1, column=1, pady=(0, 6))

        self.buttonframe = Frame(self)
        self.buttonframe.grid(row=2, column=0, columnspan=2, pady=(4, 6))

        self.logbtn = Button(self.buttonframe, text="Log in", command=self.action_login)
        self.logbtn.grid(row=0, column=0)

        self.pack()
    
    def action_login(self):
        # send information to server
        user = {}
        user["username"] = self.username.get()
        user["password"] = self.password.get()
        data = str(user)
        pk = packet(MessageType.login, data)
        msg = pk.to_message()
        self.client.send(msg)
        print("[LOGIN] Login message sent, waiting to receive authorization.")

        """ receive message from server"""
        # handle failure
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.login_fail:
            messagebox.showerror("Login fail", "Wrong username or password!")
            print("[ERROR] Wrong username or password.")
            return
        
        # handle success
        if pk.mt == MessageType.login_success:
            print("[LOGIN] Login successful.")
            client.mem.username = user["username"]
            self.master.destroy()
            bookshelf = Toplevel(client.mem.tk_root, takefocus=True)
            MainInterface(client=self.client, master=bookshelf)
            return

    def destroy_window(self):
        self.client.send(packet(MessageType.disconnect, "").to_message())
        client.mem.tk_root.destroy()
        
