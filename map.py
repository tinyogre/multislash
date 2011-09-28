
from random import randint

# W,H of whole map
MAP_SIZE=64

# Limits on room size
MIN_ROOM=5
MAX_ROOM=20

# Map of cell type to text char
textmap = \
    ' Y:?????????????' + \
    '789?????????????' + \
    '456?????????????' + \
    '123?????????????'

# Create reverse map for loading pre-drawn map
mapvals = {}
for c in xrange(len(textmap)):
    mapvals[textmap[c]] = c

SOLID_WALL = mapvals['5']

class Map:
    def __init__(self):
        self.cells = [[SOLID_WALL for x in xrange(MAP_SIZE)] for y in xrange(MAP_SIZE)]

    def load(self, text):
        y = 0
        for line in text:
            for x in xrange(len(line)):
                if line[x] in mapvals:
                    self.cells[x][y] = mapvals[line[x]]
                else:
                    self.cells[x][y] = SOLID_WALL
            y += 1

    def __str__(self):
        s = ''
        for y in xrange(MAP_SIZE):
            for x in xrange(MAP_SIZE):
                s += self.cell_char(self.cells[x][y])
            s += '\n'
        return s

    def generate(self):
        num_rooms = randint(5,20)
        for r in xrange(num_rooms):
            rx=randint(0, MAP_SIZE-1)
            ry=randint(0, MAP_SIZE-1)
            rw=randint(MIN_ROOM, MAX_ROOM)
            rh=randint(MIN_ROOM, MAX_ROOM)
            for y in xrange(rh):
                if y + ry >= MAP_SIZE:
                    break
                for x in xrange(rw):
                    if x + rx >= MAP_SIZE:
                        break
                    self.cells[x + rx][y + ry] = 0


    def cell_char(self, val):
        return textmap[val]

if __name__ == "__main__":
    m = Map()
    m.generate()
    print m,
