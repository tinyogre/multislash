
var idleTimer;
var framerate = 1000/20;
var render;
var sock;
var my_id;

function log(a) {
	$("#log").append(a+"<br/>");
}

function idle() {
	render.render();
	idleTimer = setTimeout("idle();", framerate);
}

function start_game() {

	sock = new io.Socket(window.location.hostname, {port: 8001, rememberTransport: false});
	sock.connect();

	sock.addEvent('connect', function() {
			sock.send({chat: 'Hey, I joined!'});
        });

	sock.addEvent('message', function(data) {
			if(data.chat) {
				log(data.chat);
			} else if(data.init) {
				my_id = data.init.id;
				render.set_map(data.init.map);
				render.set_loc(my_id, data.init.x, data.init.y);
			} else if(data.update) {
				render.set_loc(data.update.id, data.update.x, data.update.y);
			} else if(data.left) {
				render.set_loc(data.left.id, -1, -1);
			}
		});

	render = new slrender();
	$("#game")
		// Add tab index to ensure the canvas retains focus
		.attr("tabindex", "0")
		// Mouse down override to prevent default browser controls from appearing
		.mousedown(function(){ $(this).focus(); return false; }) 
		.keydown(function(e){ 
				switch(e.keyCode) {
					case 37: // left
						sock.send({move: 'left'});
						break;
					case 38: // up
						sock.send({move: 'up'});
						break;
					case 39: // right
						sock.send({move: 'right'});
						break;
					case 40: // down
						sock.send({move: 'down'});
						break;
				}
				return false;
			});

	// Run the first tick now, which will set itself up for more ticks
	idle();
}
