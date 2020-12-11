import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askinteger
import ast

from protocol import *
import client.mem

class ReaderForm(tk.Frame):
    def __init__(self, client, bookname, master=None):
        super().__init__(master)
        self.master = master
        self.bookname = bookname
        self.client = client
        self.page_num = 0
        self.total_page = 0
        self.chapter = []
        self.chap_num = 0
        self.total_chapter = 0
        self.createForm()
        master.protocol("WM_DELETE_WINDOW", self.update_bookmark)

    def createForm(self):
        self.master.title("Book Reader")

        self.chapbtn = Button(self, command=self.jump_chapter)
        self.chapbtn.pack(side=TOP, fill=X, expand=YES)

        self.text = Text(self, height=35)
        self.text.pack(side=TOP, fill=BOTH)
        self.read()

        self.buttonframe = Frame(self)
        self.buttonframe.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.prechap = Button(self.buttonframe, text="Prev Chap", command=self.previous_chapter)
        self.prechap.pack(side=LEFT, fill=X, expand=YES)
        self.prepg = Button(self.buttonframe, text="Prev Page", command=self.previous_page)
        self.prepg.pack(side=LEFT, fill=X, expand=YES)
        self.pagebtn = Button(self.buttonframe, text=str(self.page_num+1) + '/' + str(self.total_page+1), command=self.jump_page)
        self.pagebtn.pack(side=LEFT, fill=X, expand=YES)
        self.nxtpg = Button(self.buttonframe, text="Next Page", command=self.next_page)
        self.nxtpg.pack(side=LEFT, fill=X, expand=YES)
        self.nxtchap = Button(self.buttonframe, text="Next Chap", command=self.next_chapter)
        self.nxtchap.pack(side=LEFT, fill=X, expand=YES)

        self.pack()

    def get_chapter(self):
        """Get chapter number of the page

        Returns:
            int: chapter number of the page
        """
        if self.page_num == 0:
            return 0
        for i in range(self.total_chapter):
            if self.page_num >= self.chapter[i][1]:
                if i == self.total_chapter - 1 or self.page_num < self.chapter[i+1][1]:
                    return i

    def read(self):
        """Start to read and ready to receive book and detail from server.
        """
        # send request to the server
        data = {
            "username": client.mem.username,
            "bookname": self.bookname,
        }
        data = str(data)
        msg = packet(mt=MessageType.read, data=data).to_message()
        self.client.send(msg)

        # receive bookmark
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.page_num:
            self.page_num = int(pk.data)
            print("[BOOKMARK] Last read page %d" % self.page_num)
        else:
            print("[ERROR] Get bookmark failed.")
            messagebox.showerror("Error","Failed to get bookmark.")
            return
        
        # receive total page number
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.total_page:
            self.total_page = int(pk.data)
            print("[TOTALPAGE] Total page of the book is: %d" % self.total_page)
        else:
            print("[ERROR] Get total page failed.")
            messagebox.showerror("Error","Failed to get total page.")
            return
        
        # receive chapter list
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.chap_list:
            self.chapter = ast.literal_eval(pk.data)
            # print(self.chapter)
            self.total_chapter = len(self.chapter)
            self.chap_num = self.get_chapter()
            self.chapbtn['text'] = self.chapter[self.chap_num][0]
            print("[CHAPLIST] Chapter list received.")
        else:
            print("[ERROR] Get chapter list failed.")
            messagebox.showerror("Error","Failed to get chapter list.")
            return
        
        # receive page
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        txt = pk.data
        if pk.mt == MessageType.send_page:
            print("[RECV] Page received.")
            if txt[0] == "#":
                txt = txt[1:]
            self.text.insert(1.0, txt)
        else:
            print("[ERROR] Page not received.")
            messagebox.showerror("Error", "Page not received.")
        return

    def ask_chap(self):
        """Ask client to input the chapter to jump.

        Returns:
            chap_name: chapter name to jump
        """
        dialog = ChapterList(self.chapter)
        self.wait_window(dialog)
        return dialog.chap_name

    def jump_chapter(self):
        """Jump to the chapter page.
        """
        chap_name = self.ask_chap()
        if chap_name is None:
            return
        for i in range(self.total_chapter):
            if chap_name == self.chapter[i][0]:
                self.chap_num = i
                self.page_num = self.chapter[self.chap_num][1]
                self.pagebtn['text'] = str(self.page_num+1) + '/' + str(self.total_page+1)
                self.chapbtn['text'] = self.chapter[self.chap_num][0]       

                self.client.send(packet(MessageType.require_page, self.bookname + ' ' + str(self.page_num)).to_message())
                msg = self.client.recv(config["packet"]["size"])
                pk = packet().to_packet(msg)
                if pk.mt == MessageType.send_page:
                    print("[RECV] Page received.")
                    self.text.delete('1.0', 'end')
                    txt = pk.data
                    if txt[0] == '#':
                        txt = txt[1:]
                    self.text.insert(1.0, txt)
                else:
                    messagebox.showerror('Error','Chapter not received.')
                return

    def jump_page(self):
        """Jump to the required page.
        """
        self.page_num = askinteger('Jump page', 'Page', initialvalue=self.page_num+1, maxvalue=self.total_page + 1, minvalue=1) - 1
        self.client.send(packet(MessageType.require_page, self.bookname + ' ' + str(self.page_num)).to_message())
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.send_page:
            print("[RECV] Page received.")
            self.chap_num = self.get_chapter()
            self.chapbtn['text'] = self.chapter[self.chap_num][0]
            self.pagebtn['text'] = str(self.page_num+1) + '/' + str(self.total_page+1)
            self.text.delete('1.0', 'end')
            txt = pk.data
            if txt[0] == '#':
                txt = txt[1:]
            self.text.insert(1.0, txt)
        else:
            messagebox.showerror('Error','Page not received.')
        return


    def previous_chapter(self):
        """Turn to previous chapter page.
        """
        if self.chap_num == 0:
            messagebox.showwarning('Warning','No previous chapter.')
            return
        self.chap_num = self.chap_num - 1
        self.page_num = self.chapter[self.chap_num][1]
        self.pagebtn['text'] = str(self.page_num + 1) + '/' + str(self.total_page + 1)
        self.chapbtn['text'] = self.chapter[self.chap_num][0]

        self.client.send(packet(MessageType.require_page, self.bookname + ' ' + str(self.page_num)).to_message())
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.send_page:
            print("[RECV] Chapter received.")
            self.text.delete('1.0', 'end')
            txt = pk.data
            if txt[0] == '#':
                txt = txt[1:]
            self.text.insert(1.0, txt)
        else:
            messagebox.showerror('Error','Previous chapter not received.')
        return

    def previous_page(self):
        """Turn to the previous page.
        """
        if self.page_num == 0:
            messagebox.showwarning('Warning','No previous page.')
            return
        self.page_num = self.page_num - 1

        self.client.send(packet(MessageType.require_page, self.bookname + ' ' + str(self.page_num)).to_message())
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.send_page:
            print("[RECV] Chapter received.")
            self.chap_num = self.get_chapter()
            self.chapbtn['text'] = self.chapter[self.chap_num][0]
            self.pagebtn['text'] = str(self.page_num + 1) + '/' + str(self.total_page + 1)
            self.text.delete('1.0', 'end')
            txt = pk.data
            if txt[0] == '#':
                txt = txt[1:]
            self.text.insert(1.0, txt)
        else:
            messagebox.showerror('Error','Previous page not received.')
        return

    def next_page(self):
        """Turn to next page.
        """
        if self.page_num == self.total_page:
            messagebox.showwarning('Warning','No next page.')
            return
        self.page_num = self.page_num + 1

        self.client.send(packet(MessageType.require_page, self.bookname + ' ' + str(self.page_num)).to_message())
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.send_page:
            print("[RECV] Page received.")
            self.chap_num = self.get_chapter()
            self.chapbtn['text'] = self.chapter[self.chap_num][0]
            self.pagebtn['text'] = str(self.page_num + 1) + '/' + str(self.total_page + 1)
            self.text.delete('1.0', 'end')
            txt = pk.data
            if txt[0] == '#':
                txt = txt[1:]
            self.text.insert(1.0, txt)
        else:
            messagebox.showerror('Error','Next page not received.')
        return

    def next_chapter(self):
        """Turn to next chapter page.
        """
        if self.chap_num >= self.total_chapter - 1:
            messagebox.showwarning('Warning','No next chapter.')
            return
        self.chap_num = self.chap_num + 1
        self.page_num = self.chapter[self.chap_num][1]
        self.pagebtn['text'] = str(self.page_num + 1) + '/' + str(self.total_page + 1)
        self.chapbtn['text'] = self.chapter[self.chap_num][0]

        self.client.send(packet(MessageType.require_page, self.bookname + ' ' + str(self.page_num)).to_message())
        msg = self.client.recv(config["packet"]["size"])
        pk = packet().to_packet(msg)
        if pk.mt == MessageType.send_page:
            print("[RECV] Chapter received.")
            self.text.delete('1.0', 'end')
            txt = pk.data
            if txt[0] == '#':
                txt = txt[1:]
            self.text.insert(1.0, txt)
        else:
            messagebox.showerror('Error','Next chapter not received.')
        return
    
    def update_bookmark(self):
        """Update bookmark when closing the window.
           A substitute for destroy_window().
        """
        self.client.send(packet(MessageType.update_bookmark, client.mem.username + ' ' + self.bookname + ' ' + str(self.page_num)).to_message())
        self.master.destroy()
        return

"""Chapter list UI"""
class ChapterList(tk.Toplevel):
    def __init__(self, chapter):
        super().__init__()
        self.chapter = chapter
        self.chap_name = ''
        self.createForm()        

    def createForm(self):
        self.title("Chapters")

        self.sb = Scrollbar(self)
        self.sb.pack(side=RIGHT, fill=Y)

        self.chaplist = Listbox(self, height=15, width=40, yscrollcommand=self.sb.set)
        for chap in self.chapter:
            self.chaplist.insert(END, chap[0])
        self.chaplist.pack(side=TOP, fill=BOTH)
        
        self.sb.config(command=self.chaplist.yview)

        self.buttonframe = Frame(self)
        self.buttonframe.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.jmpbtn = Button(self.buttonframe, text="Jump", command=self.jump)
        self.jmpbtn.pack(side=LEFT, fill=X, expand=YES)
        self.cncbtn = Button(self.buttonframe, text="Cancel", command=self.cancel)
        self.cncbtn.pack(side=LEFT, fill=X, expand=YES)

    def jump(self):
        self.chap_name = self.chaplist.get(self.chaplist.curselection())
        self.destroy()

    def cancel(self):
        self.destroy()