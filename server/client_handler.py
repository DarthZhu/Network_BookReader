# import json
import os

from protocol.protocol import *
from utils import get_users

#TODO
def login(conn, data):
    data = eval(data)
    username = data["username"]
    password = data["password"]
    users = get_users()
    if username not in users.keys():
        pk = packet(MessageType.login_fail, "User not exist.")
        msg = pk.to_message()
        conn.send(msg)
        return
    if users[username] != password:
        pk = packet(MessageType.login_fail, "Password incorrect.")
        msg = pk.to_message()
        conn.send(msg)
        return
    pk = packet(MessageType.login_success, "")
    msg = pk.to_message()
    conn.send(msg)
    print("[LOGIN] Login successful")
    return

def require_list(conn, data):
    data = ""
    booklist = os.listdir("./server/books")
    for bookname in booklist:
        bookname = bookname.strip(".txt")
        data += bookname
        data += " "
    data = data[0: len(data) - 1]
    msg = packet(mt=MessageType.send_list, data=data).to_message()
    conn.send(msg)
    print("[SENDING] Booklist sent.")

def download(conn, data):
    pass

def read(conn, data):
    pass

def require_page(conn, data):
    pass

def require_chapter(conn, data):
    pass

def update_bookmark(conn, data):
    pass

def handler_dispatch(conn, mt, data):
    handler = {
        MessageType.login: login,
        MessageType.donwload: download,
        MessageType.read: read,
        MessageType.require_page: require_page,
        MessageType.require_list: require_list,
        MessageType.require_chapter: require_chapter,
        MessageType.update_bookmark: update_bookmark,
    }
    func = handler.get(mt)
    func(conn, data)

