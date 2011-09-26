
var idleTimer;
var framerate = 1000/60;
var render;

function log(a) {
	$("#log").append(a+"<br/>");
}

function idle() {
	render.render();
	idleTimer = setTimeout("idle();", framerate);
}

function start_game() {

	render = new slrender();
	$("#game")
		// Add tab index to ensure the canvas retains focus
		.attr("tabindex", "0")
		// Mouse down override to prevent default browser controls from appearing
		.mousedown(function(){ $(this).focus(); return false; }) 
		.keydown(function(e){ 
				switch(e.keyCode) {
					case 37: // left
						render.plx--;
						break;
					case 38: // up
						render.ply--;
						break;
					case 39: // right
						render.plx++;
						break;
					case 40: // down
						render.ply++;
						break;
				}
				return false; 
			});

	// Run the first tick now, which will set itself up for more ticks
	idle();
}
