
function slrender() {
	this.canvas = $("#game")[0];
	this.ctx = this.canvas.getContext("2d");
	this.tilesize = 16;
	this.width = 1024;
	this.height = 1024;

	this.viewwidth = this.width / this.tilesize;
	this.viewheight = this.height / this.tilesize;
	this.imagesLoaded = false;

	this.sprites = new Image();
	this.sprites.onload = (function(r) { r.imagesLoaded = true; }(this));
	this.sprites.src = '/static/images/spritesheet.png';
	this.spritesPerLine = 16;

	this.locs = new Array();

	this.set_loc = function(id, x, y) {
		this.locs[id] = [x, y];
	}

	this.get_tile = function(x, y) {
		for(var i = 0; i < this.locs.length; i++) {
			if(this.locs[i]) {
				if(this.locs[i][0] == x && this.locs[i][1] == y) {
					return 1;
				}
			}
		}
		if(x >= this.map.length || y >= this.map[x].length) {
			return -1;
		} else {
			return this.map[x][y]
		}
	}

	this.set_map = function(map) {
		this.map = map;
		x = 0
	}
				
	this.render = function() {
		this.ctx.fillStyle="rgb(0,0,0)";
		this.ctx.fillRect(0,0,this.width, this.height);
		
		if(!this.imagesLoaded || !this.map) {
			return;
		}

		for(var y = 0; y < this.viewheight; y++) {
			for(var x = 0; x < this.viewwidth; x++) {
				var spid = this.get_tile(x, y);
				if(spid < 0) {
					continue;
				}
				this.ctx.drawImage(this.sprites, 
								   (spid % this.spritesPerLine) * this.tilesize,
								   Math.floor(spid / this.spritesPerLine) * this.tilesize,
								   this.tilesize, this.tilesize,
								   x * this.tilesize, y * this.tilesize, this.tilesize, this.tilesize);
			}
		}
	}
}

