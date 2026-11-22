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

    def update_edge(self, bearing, new_edge):
        match bearing:
            case 1:
                self.posX = new_edge
                new_edge.next.negX = Edge(self, new_edge.distance)
            case 2:
                self.negX = new_edge
                new_edge.next.posX = Edge(self, new_edge.distance)
            case 3:
                self.posY = new_edge
                new_edge.next.negY = Edge(self, new_edge.distance)
            case 4:
                self.negY = new_edge
                new_edge.next.posY = Edge(self, new_edge.distance)
            case 5:
                self.pozZ = new_edge
                new_edge.next.negZ = Edge(self, new_edge.distance)
            case 6:
                self.negZ = new_edge
                new_edge.next.posZ = Edge(self, new_edge.distance)

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

def checkAxis(matrix, graph, node, axis, mode):
    pos_node = None
    neg_node = None
    contPos, contNeg = True
    pos = node.pos.copy()
    neg = node.pos.copy()
    while True:
        if contPos:
            pos[axis] += 1
            if matrix[pos[0]][pos[1]][pos[2]] != mode:
                contPos = False
            else:
                positionString = getPositionString(pos)
                if positionString in graph:
                    pos_node = graph[positionString]
                    contPos = False
        if contNeg:
            neg[axis] -= 1
            if matrix[neg[0]][neg[1]][neg[2]] != mode:
                contNeg = False
            else:
                positionString = getPositionString(neg)
                if positionString in graph:
                    neg_node = graph[positionString]
                    contNeg = False
        if not (contPos or contNeg):
            if pos_node != None:
                pos_dist = abs(pos[axis] - node.pos[axis])
                node.update_edge(axis * 2 + 1, Edge(pos_node, pos_dist))
            if neg_node != None:
                neg_dist = abs(neg[axis - node.pos[axis]])
                node.update_edge(axis * 2 + 2, Edge(neg_node, neg_dist))
            break