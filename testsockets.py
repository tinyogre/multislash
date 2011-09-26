#!/usr/bin/env python

import tornadio, tornadio.server
import tornado.web

class MyConnection(tornadio.SocketConnection):
    def on_message(self,message):
        print message

MyRouter = tornadio.get_router(MyConnection)

application = tornado.web.Application(
    [MyRouter.route()],
    socket_io_port=9000)

socketio_server = tornadio.server.SocketServer(application)

#application.listen(8888)
#tornado.ioloop.IOLoop.instance().start()
