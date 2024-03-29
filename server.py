from os import path as op
import os

import tornado.web
import tornadio
import tornadio.router
import tornadio.server
import simplejson

from map import Map, SOLID_WALL
import testmap

ROOT = op.normpath(op.dirname(__file__))

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("index.html")

next_id = 1

class Server:
    participants = set()

    def __init__(self):
        self.map = Map()
        self.map.generate()

    def send(self, player, packet):
        print simplejson.dumps(packet)
        player.send(packet)

    def broadcast(self, packet):
        print 'broadcast: ' + simplejson.dumps(packet)
        for p in self.participants:
            p.send(packet)

server = Server()

class PlayerConn(tornadio.SocketConnection):
    def on_open(self, *args, **kwargs):
        global next_id
        server.participants.add(self)
        self.id = next_id;
        print 'Created player ' + str(self.id)
        next_id += 1;
        self.x = server.map.start[0]
        self.y = server.map.start[1]
        packet = {'init': {'id': self.id,
                           'x': self.x, 
                           'y': self.y,
                           'map': server.map.cells}}
        server.send(self, packet)
        
    def on_message(self, message):
        if 'move' in message:
            nx = self.x
            ny = self.y
            dir = message['move']
            if dir == 'left':
                nx -= 1
            elif dir == 'up':
                ny -= 1
            elif dir== 'right':
                nx += 1
            elif dir == 'down':
                ny += 1
            if not server.map.is_passable(nx, ny, self):
                return

            self.x = nx
            self.y = ny

        for p in server.participants:
            server.send(p, {'update': {'id': self.id,
                                       'x': self.x,
                                       'y': self.y}})
        server.map.tick(server)


    def on_close(self):
        server.participants.remove(self)
        packet = {'left': {'id': self.id}}
        for p in server.participants:
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

