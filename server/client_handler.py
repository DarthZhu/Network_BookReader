# import json
import os
import math

from protocol.protocol import *
from utils import get_bookmarks, get_users

ONE_PAGE_WORDS = 1000

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
    bookname = data
    path = "./server/books/" + bookname + ".txt"
    with open(path, "rb") as f:
        size = config["packet"]["size"] - len("000".encode(config["packet"]["format"]))
        while True:
            data = f.read(size)
            if not data:
                break
            msg = packet(mt=MessageType.send_book, data=data).to_message_no_encode()
            conn.send(msg)
    conn.send(packet(mt=MessageType.send_book_done, data="").to_message())
    print("[SENDBOOK] Send book done.")
        

def send_page(conn, bookname, page_num):
    path = "./server/books/" + bookname + ".txt"
    with open(path, "r", encoding='utf-8') as f:
        page_words = ONE_PAGE_WORDS
        num = 0
        j = 0
        line = f.readline()
        s = ''
        while num <= page_num:
            s = ''
            if line:
                s += line
                line = f.readline()
                while line:
                    if line[0] == '#':
                        break
                    s += line
                    line = f.readline()
            if num + math.ceil(len(s) / page_words) - 1 < page_num:
                num += math.ceil(len(s) / page_words)
                continue
            elif num + math.ceil(len(s) / page_words) - 1 == page_num:
                j = page_words * (math.ceil(len(s) / page_words) - 1)
                num = num + math.ceil(len(s) / page_words)
            else:
                j = page_words * (page_num - num)
                num = page_num
                break
        conn.send(packet(MessageType.send_page, s[j: j+page_words]).to_message())
        print("[SEND] Send page %d." % page_num)
    return

def read(conn, data):
    info = eval(data)
    username = info["username"]
    bookname = info["bookname"]

    # send page number of the bookmark
    page_num = 0
    bookmarks = get_bookmarks()
    try:
        bookmark = bookmarks[username].strip("\n")
        bookmark = bookmark.split("|")
        if bookname in bookmark:
            index = bookmark.index(bookname)
            page_num = int(bookmark[index + 1])
    except:
        page_num = 0

    msg = packet(MessageType.page_num, data=page_num).to_message()
    conn.send(msg)
    
    # send total page and chapter list
    total_page = 0
    chapter = []
    # i = 1
    with open('./server/books/' + bookname + '.txt', 'r', encoding='utf-8') as f:
        page_words = ONE_PAGE_WORDS
        line = f.readline()
        while line:
            s = ''
            s += line
            line = f.readline()
            while line:
                if line[0] == '#':
                    break
                s += line
                line = f.readline()
            chapter_name = ""
            for word in s:
                if word == '\n':
                    break
                chapter_name += word
            chapter.append([chapter_name[1:], total_page])
            total_page += math.ceil(len(s) / page_words)
    # print(chapter)
    conn.send(packet(MessageType.total_page, str(total_page - 1)).to_message())
    conn.send(packet(MessageType.chap_list, str(chapter[:])).to_message())
    print("[CHAP] Book %s chapter sent." % bookname)
    
    # send page of bookmarks
    send_page(conn, bookname, page_num)

def require_page(conn, data):
    data = data.split(" ")
    bookname = data[0]
    page_num = int(data[1])
    send_page(conn, bookname, page_num)
    return

def update_bookmark(conn, data):
    bookmark = data.split(" ")
    username = bookmark[0]
    bookname = bookmark[1]
    page_num = bookmark[2]
    with open('./server/storage/bookmarks.txt', 'r', encoding='utf-8') as f:
        users = f.read().splitlines()
        for i in range(len(users)):
            user_lst = users[i].split(' ')
            if user_lst[0] == username:
                booklist = user_lst[1].split('|')
                index = booklist.index(bookname) if (bookname in booklist) else -1
                if index == -1:
                    users[i] = users[i] + '|' + bookname + '|' + page_num
                else:
                    booklist[index + 1] = page_num
                    temp_string = username + " "
                    for b in booklist:
                        temp_string += b
                        temp_string +="|"
                    users[i] = temp_string.strip("|")
                break
    with open('./server/storage/bookmarks.txt', 'w', encoding='utf-8') as f:
        users = '\n'.join(users) + '\n'
        f.write(users)



def handler_dispatch(conn, mt, data):
    handler = {
        MessageType.login: login,
        MessageType.download: download,
        MessageType.read: read,
        MessageType.require_page: require_page,
        MessageType.require_list: require_list,
        MessageType.update_bookmark: update_bookmark,
    }
    func = handler.get(mt)
    func(conn, data)

