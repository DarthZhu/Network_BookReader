import socket
import sys
import tkinter as tk

from protocol import *
from utils import get_config
from client.interfaces.login_interface import LoginInterface
import client.mem as mem

def init_client():
    """Initiate client and connect to the server
    """
    config = get_config()
    root = tk.Tk()
    mem.tk_root = root
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((config["client"]["server_ip"], config["client"]["server_port"]))
    except socket.error:
        print("[ERROR] Connecting to server failed.")
        sys.exit()
    # pk = packet(MessageType.login, "1")
    # client.send(pk.to_message())
    # input()
    login = tk.Toplevel(root)
    LoginInterface(client, master=login)
    root.withdraw()
    root.mainloop()
    try:
        root.destroy()
    except tk.TclError:
        pass