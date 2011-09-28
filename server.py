from os import path as op
import os

import tornado.web
import tornadio
import tornadio.router
import tornadio.server
import simplejson

from map import Map
import testmap

ROOT = op.normpath(op.dirname(__file__))

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("index.html")

next_id = 1

class Server:
    def __init__(self):
        self.map = Map()
        self.map.generate()

    def send(self, player, packet):
        print simplejson.dumps(packet)
        player.send(packet)

server = Server()

class PlayerConn(tornadio.SocketConnection):
    # Class level variable
    participants = set()

    def on_open(self, *args, **kwargs):
        global next_id
        self.participants.add(self)
        self.id = next_id;
        print 'Created player ' + str(self.id)
        next_id += 1;
        self.x = 30;
        self.y = 22;
        packet = {'init': {'id': self.id,
                           'x': self.x, 
                           'y': self.y,
                           'map': server.map.cells}}
        server.send(self, packet)
        
    def on_message(self, message):
        if 'move' in message:
            dir = message['move']
            if dir == 'left':
                self.x -= 1
            elif dir == 'up':
                self.y -= 1
            elif dir== 'right':
                self.x += 1
            elif dir == 'down':
                self.y += 1

        for p in self.participants:
            server.send(p, {'update': {'id': self.id,
                                       'x': self.x,
                                       'y': self.y}})

    def on_close(self):
        self.participants.remove(self)
        packet = {'left': {'id': self.id}}
        for p in self.participants:
            server.send(p, packet)

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

#use the routes classmethod to build the correct resource
ChatRouter = tornadio.get_router(PlayerConn)

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

