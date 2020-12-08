from client.interfaces.read_interface import ReaderForm
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory

import client.mem
from protocol.protocol import *

class MainInterface(tk.Frame):
    def __init__(self, client, master=None):
        super().__init__(master)
        self.master = master
        self.client = client
        self.createForm()
        master.protocol("WM_DELETE_WINDOW", self.destroy_window)

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
        """Jump to reading interface
        """
        book = self.booklist.get(self.booklist.curselection())
        read = Toplevel(client.mem.tk_root, takefocus=True)
        ReaderForm(self.client, book, read)

    def download(self):
        """Download the selected book
        """
        path = askdirectory()
        if not path:
            return
        bookname = self.booklist.get(self.booklist.curselection())
        self.client.send(packet(MessageType.download, bookname).to_message())
        print("[DOWNLOAD] Downloading book %s" % bookname)        

        path += "/" + bookname + ".txt"
        with open(path, "wb") as f:
            while True:
                msg = self.client.recv(config["packet"]["size"])
                pk = packet().to_packet_no_decode(msg)
                if pk.mt == MessageType.send_book:
                    f.write(pk.data)
                elif pk.mt == MessageType.send_book_done:
                    break
                else:
                    messagebox.showerror("Error", "Download failed.")
        print("[DOWNLOAD] Download complete.")
        return

    def destroy_window(self):
        client.mem.tk_root.destroy()

