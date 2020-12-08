import json

def get_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
    return config

def get_users():
    users = {}
    with open("server/storage/users.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            s = line.split(' ')
            users[s[0]] = s[1]
    return users

def get_bookmarks():
    users = {}
    with open("server/storage/bookmarks.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            s = line.split(' ')
            users[s[0]] = s[1]
    return users