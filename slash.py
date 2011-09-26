from os import path as op
import os

import tornado.web
import tornadio
import tornadio.router
import tornadio.server

ROOT = op.normpath(op.dirname(__file__))

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("index.html")

# FIXME should not be writing code for this, serve it from a plain old http server
class StaticHandler(tornado.web.RequestHandler):
    def get(self, aaa):
        print "GET " + aaa
        print self.request
        self.render("static/" + aaa)

class ChatConnection(tornadio.SocketConnection):
    # Class level variable
    participants = set()

    def on_open(self, *args, **kwargs):
        self.participants.add(self)
        self.send("Welcome!")

    def on_message(self, message):
        for p in self.participants:
            p.send(message)

    def on_close(self):
        self.participants.remove(self)
        for p in self.participants:
            p.send("A user has left.")

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

#use the routes classmethod to build the correct resource
ChatRouter = tornadio.get_router(ChatConnection)

#configure the Tornado application
application = tornado.web.Application(
    [(r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])), 
     (r"/", IndexHandler), 
     ChatRouter.route()],
    enabled_protocols = ['websocket',
                         'flashsocket',
                         'xhr-multipart',
                         'xhr-polling'],
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8001
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    tornadio.server.SocketServer(application)

