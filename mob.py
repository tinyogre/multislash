from random import randint
next_id = 1
class Mob:
    def __init__(self, x, y, type):
        global next_id
        self.x = x
        self.y = y
        self.type = type
        self.id = next_id
        next_id += 1

    def tick(self, server, map):
        dir = randint(1,4)
        nx = self.x
        ny = self.y
        if dir == 1:
            ny = self.y - 1
        elif dir == 2:
            nx = self.x + 1
        elif dir == 3:
            ny = self.y + 1
        else:
            nx = self.x - 1

        if map.is_passable(nx,ny,self):
            self.x = nx
            self.y = ny
        server.broadcast({'mobupdate': {'id': self.id,
                                        'type': 2, # HACK FIXME
                                        'x': self.x,
                                        'y': self.y}})
