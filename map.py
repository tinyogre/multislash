
from random import randint

# W,H of whole map
MAP_SIZE=64

# How many rooms?  (Counts failures too!)
NUM_ROOMS = 500

# Limits on room size
MIN_ROOM=5
MAX_ROOM=10

MAX_HALL=10

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

class Room:
    types = ['rect',
             'hall']
             
    def __init__(self, type, x, y, w, h):
        self.type = type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def pick_random_wall(self):
        if self.type == 'rect' or self.type == 'hall':
            # CSS order, top, right, bottom, left
            wall = randint(1,4)
            if wall == 1 or wall == 3:
                x = randint(self.x, self.x + self.w - 1)
                if wall == 1:
                    y = self.y - 1
                else:
                    y = self.y + self.h
            if wall == 2 or wall == 4:
                y = randint(self.y, self.y + self.h - 1)
                if wall == 2:
                    x = self.x + self.w
                else:
                    x = self.x - 1

            return (x,y,wall)
    def __str__(self):
        return "(%d,%d) (%dx%d)" % (self.x, self.y, self.w, self.h)
                
class Map:
    def __init__(self):
        self.cells = [[SOLID_WALL for x in xrange(MAP_SIZE)] for y in xrange(MAP_SIZE)]

    # This was used for early testing, but if it gets that far, I'd like to have set pieces loaded
    # here too
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

    def excavate(self, room):
        if room.type == 'rect' or room.type == 'hall':
            for y in xrange(room.h):
                if y + room.y >= MAP_SIZE - 1:
                    break
                for x in xrange(room.w):
                    if x + room.x >= MAP_SIZE - 1:
                        break
                    self.cells[x+room.x][y+room.y] = 0
        
        self.rooms.append(room)

    def space_is_clear(self, x, y, w, h):
        for chky in xrange(h):
            if chky + y < 1 or chky + y >= MAP_SIZE - 2:
                print 'oob'
                return False
            for chkx in xrange(w):
                if chkx + x < 1 or chkx + x >= MAP_SIZE - 2:
                    print 'oob'
                    return False

                if self.cells[chkx + x][chky + y] != SOLID_WALL:
                    print "(%d,%d): %d" %(chkx + x, chky + y, self.cells[chkx + x][chky + y])
                    return False
        print 'clear!'
        return True

    def generate_branching(self):
        self.rooms = []
        # Start with a simple rectangular room
        r = Room('rect',
                 MAP_SIZE / 2, MAP_SIZE/2,
                 randint(MIN_ROOM, MAX_ROOM),
                 randint(MIN_ROOM, MAX_ROOM))
        self.excavate(r)

        for ri in xrange(NUM_ROOMS - 1):
            # Pick a room to branch off from
            startroom = self.rooms[randint(0, len(self.rooms) - 1)]
            
            print startroom

            # Decide where to add something
            branchloc = startroom.pick_random_wall()
            
            print branchloc

            # Decide what kind of feature to add
            type = Room.types[randint(0, len(Room.types) - 1)]
            
            print type

            if type == 'rect':
                w = randint(MIN_ROOM, MAX_ROOM)
                h = randint(MIN_ROOM, MAX_ROOM)
                print "%dx%d" %(w,h)
                if not self.space_is_clear(branchloc[0], branchloc[1], w, h):
                    continue
                self.excavate(Room(type, branchloc[0], branchloc[1], w, h))
            elif type == 'hall':
                if branchloc[2] == 1:
                    x = branchloc[0]
                    y = randint(branchloc[1] - MAX_HALL, branchloc[1] - 1)
                    w = 1
                    h = branchloc[1] - y + 1
                elif branchloc[2] == 2:
                    x = branchloc[0]
                    y = branchloc[1]
                    w = randint(2, MAX_HALL)
                    h = 1
                elif branchloc[2] == 3:
                    x = branchloc[0]
                    y = branchloc[1]
                    w = 1
                    h = randint(2, MAX_HALL)
                elif branchloc[2] == 4:
                    x = randint(branchloc[0] - MAX_HALL, branchloc[0] - 1)
                    y = branchloc[1]
                    h = 1
                    w = branchloc[0] - x + 1
                if not self.space_is_clear(x, y, w, h):
                    continue
                self.excavate(Room(type, x, y, w, h))

    def generate(self):
        self.generate_branching()

    def cell_char(self, val):
        return textmap[val]

if __name__ == "__main__":
    m = Map()
    m.generate()
    print m,
