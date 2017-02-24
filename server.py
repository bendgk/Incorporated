import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen
import time
import json

import json

users = {}

def init():
    with open('users.json', 'r') as data_file:
        users = json.load(data_file)

def create_user(name, passwd):
    if name not in users:
        users[name] = {
            "pass": passwd,
            }
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
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
        self.finish

application = tornado.web.Application([
    (r"/createUser", UserHandler),
    ])

if __name__ == '__main__':
    init()
    application.listen(7777)
    IOLoop.instance().start()
