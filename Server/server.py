import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen
import time
import json
import hashlib
import random

user_info = {}
user_data = {}

def init():
    with open('users/user_info.json', 'r') as data_file:
        user_info = json.load(data_file)
        data_file.close()

    with open('users/user_data.json', 'r') as data_file:
        user_data = json.load(data_file)
        data_file.close()

def create_salt():
    alphanum = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = ""

    for i in range(16):
        chars = chars + random.choice(alphanum)

    return chars

def hash_SHA256(pwd):
    hash_object = hashlib.sha256(pwd)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def create_user(name, pwd):
    if name not in user_info:

        salt = create_salt()

        user_info[name] = {
            'hash': hash_SHA256(pwd + salt),
            'salt': salt,
        }

        user_data[name] = {
            'money': 100
        }

        with open('users/user_info.json', 'w') as outfile:
            json.dump(user_info, outfile)
            outfile.close()

        with open('users/user_data.json', 'w') as outfile:
            json.dump(user_data, outfile)
            outfile.close()

        return True

    else:
        return "You dun goofed. (Randolph Xia, 2017)"


class UserHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        name = self.get_argument('user')
        passwd = self.get_argument('password')
        response = create_user(name, passwd)
        self.write(str(response))
        self.finish()

    def get(self):
        name = self.get_argument('user')
        response = user_data[name]
        self.write(response)
        self.finish()

application = tornado.web.Application([
    (r"/user", UserHandler),
    ])

if __name__ == '__main__':
    init()
    application.listen(7777)
    IOLoop.instance().start()
