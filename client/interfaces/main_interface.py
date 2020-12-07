import tkinter as tk
from tkinter import *
from tkinter import messagebox

import client.mem
from protocol.protocol import *

class MainInterface(tk.Frame):
    def __init__(self, client, master=None):
        super().__init__(master)
        self.master = master
        self.client = client
        self.createForm()

    def createForm(self):
        self.master.title("Bookshelf")

        self.sb = Scrollbar(self)
        self.sb.pack(side=RIGHT, fill=Y)

        self.booklist = Listbox(self, height=15, width=30, yscrollcommand=self.sb.set)
        bklist = self.get_booklist()
        for bkname in bklist:
            self.booklist.insert(END, bkname)
        self.booklist.pack(side=LEFT, fill=BOTH, expand=YES)
        
        self.sb.config(command=self.booklist.yview)

        self.buttonframe = Frame(self)
        self.buttonframe.pack(side=RIGHT, fill=BOTH, expand=YES)
        # self.refreshbtn = Button(self.buttonframe, text="Refresh", command=self.refresh)
        # self.refreshbtn.pack(side=TOP, fill=Y, expand=YES)
        self.readbtn = Button(self.buttonframe, text="Read", command=self.read)
        self.readbtn.pack(side=TOP, fill=Y, expand=YES)
        self.dlbtn = Button(self.buttonframe, text="Download", command=self.download)
        self.dlbtn.pack(side=TOP, fill=Y, expand=YES)

        self.pack()
    
    def get_booklist(self):
        """Request booklist from the server
        """
        # send request
        pk = packet(mt=MessageType.require_list, data="")
        msg = pk.to_message()
        self.client.send(msg)

        # waiting for response
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.send_list:
            booklist = pk.data.split(' ')
            print("[RECEIVED] Booklist received")
            return booklist
        else:
            print("[ERROR] Request booklist failed.")
            messagebox.showerror("Request booklist failed", "Request booklist failed.")
            return
    
    def read(self):
        pass

    def download(self):
        pass

