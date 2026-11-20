import mazecarver

DEPARTING = 0
APPROACHING = 1

def getPositionString(coord_list):
    return str(coord_list[0]) + str(coord_list[1]) + str(coord_list[2])

def getDistance(bearing, initial, end):
    match bearing:
        case 1 | 2:
            return abs(initial[0] - end[0])
        case 3 | 4:
            return abs(initial[1] - end[1])
        case 5 | 6:
            return abs(initial[2] - end[2])

class Graph:
    def __init__(self, dict):
        self.start = None
        self.dict = dict

class Edge:
    def __init__(self, next, distance):
        self.next = next
        self.distance = distance

class Node:
    def __init__(self, pos, posX=None, negX=None, posY=None, negY=None, posZ=None, negZ=None):
        self.pos = pos
        self.posX = posX
        self.negX = negX
        self.posY = posY
        self.negY = negY
        self.posZ = posZ
        self.negZ = negZ

    def update_edge(self, bearing, new_edge, mode):
        match bearing:
            case 1:
                if mode == DEPARTING:
                    self.posX = new_edge
                elif mode == APPROACHING:
                    self.negX = new_edge
            case 2:
                if mode == DEPARTING:
                    self.negX = new_edge
                elif mode == APPROACHING:
                    self.posX = new_edge
            case 3:
                if mode == DEPARTING:
                    self.posY = new_edge
                elif mode == APPROACHING:
                    self.negY = new_edge
            case 4:
                if mode == DEPARTING:
                    self.negY = new_edge
                elif mode == APPROACHING:
                    self.posY = new_edge
            case 5:
                if mode == DEPARTING:
                    self.posZ = new_edge
                elif mode == APPROACHING:
                    self.negZ = new_edge
            case 6:
                if mode == DEPARTING:
                    self.negZ = new_edge
                elif mode == APPROACHING:
                    self.posZ = new_edge