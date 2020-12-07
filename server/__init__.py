import socket
# import selectors
import threading
import sys

from utils import get_config
from protocol.protocol import *
from server.client_handler import handler_dispatch

config = get_config()

# TODO
def handle_client(conn, addr):
    """Handle client data

    Args:
        conn (socket.socket): socket connected to addr
        addr (string, string): client ip address and port
    """
    print("[NEW CONNECTION] %s:%d connected." % (addr[0], addr[1]))
    connected = True
    while connected:
        msg = conn.recv(config["packet"]["size"])
        # print(msg)
        pk = packet(MessageType.init, "").to_packet(msg)
        handler_dispatch(conn, pk.mt, pk.data)



def init_server():
    """Initiate the server and create a thread for every client.
    """
    # config = get_config()
    # sel = selectors.DefaultSelector()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        s.bind((config["server"]["ip"], config["server"]["port"]))
    except socket.error:
        print("[ERROR] Binding Failed.")
        sys.exit()
    s.listen(5)
    print("[STARTING] Server listening on: %s:%d." % (config["server"]["ip"], config["server"]["port"]))

    while(True):
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[CONNECTION ACTIVATE] Current client number: %d." % (threading.active_count() - 1))