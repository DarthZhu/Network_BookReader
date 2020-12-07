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
            s = line.split(' ')
            users[s[0]] = s[1]
    return users