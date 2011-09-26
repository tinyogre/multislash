Multislash
==========

version 0.001
-------------

Licensing
---------
Copyright (c) 2011 Joe Rumsey

Released under the MIT License, see LICENSE for details

About
-----
This is a sandbox for testing websocket tech using Socket.IO and tornadio, in
the guise of an in-browser (canvas) roguelike game.

Prerequisites
-------------

Tornado and TornadIO.  They are included from their main repositories
as submodules.  If you don't want to install them system-wide, you can
install them in a virtualenv like so (use pip or easy_install to get
virtualenv first).  This is what I do.

virtualenv env
. env/bin/activate
git submodule init
git submodule update
cd tornado
python setup.py install
cd ../tornadio
python setup.py install

Remember to ". env/bin/activate" before running/working on multislash in the future

How to "play"
-------------
Run the server:
python server.py

Connect browsers to http://localhost:8001/.  Click in canvas and use arrow keys.

This version doesn't do anything but move one character per browser around.
