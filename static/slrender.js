
function slrender() {
	this.canvas = $("#game")[0];
	this.ctx = this.canvas.getContext("2d");
	this.tilesize = 16;
	this.width = 1024;
	this.height = 768;

	this.viewwidth = this.width / this.tilesize;
	this.viewheight = this.height / this.tilesize;
	this.imagesLoaded = false;

	this.sprites = new Image();
	this.sprites.onload = (function(r) { r.imagesLoaded = true; }(this));
	this.sprites.src = '/static/images/spritesheet.png';
	this.spritesPerLine = 16;

	this.plx = 16;
	this.ply = 16;

	this.get_tile = function(x, y) {
		if(x == this.plx && y == this.ply) {
			return 1;
		} else {
			return 0;
		}
	}

	this.render = function() {
		this.ctx.fillStyle="rgb(0,0,0)";
		this.ctx.fillRect(0,0,1024,768);
		
		if(!this.imagesLoaded) {
			return;
		}

		for(var y = 0; y < this.viewheight; y++) {
			for(var x = 0; x < this.viewwidth; x++) {
				var spid = this.get_tile(x, y);
				this.ctx.drawImage(this.sprites, 
								   (spid % this.spritesPerLine) * this.tilesize,
								   Math.floor(spid / this.spritesPerLine) * this.tilesize,
								   this.tilesize, this.tilesize,
								   x * this.tilesize, y * this.tilesize, this.tilesize, this.tilesize);
			}
		}
	}
}

