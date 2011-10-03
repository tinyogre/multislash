
function moblist() {
	this.mobs = new Array();
	this.update = function(packet) {
		data = packet.mobupdate
		if(this.mobs[data.id]) {
			render.remove_mob(data.id, this.mobs[data.id].x, this.mobs[data.id].y, data.type);
		}

		if(!this.mobs[data.id]) {
			this.mobs[data.id] = {};
		}

		this.mobs[data.id].x = data.x;
		this.mobs[data.id].y = data.y;

		render.add_mob(data.id, data.x, data.y, data.type);
	}
}
