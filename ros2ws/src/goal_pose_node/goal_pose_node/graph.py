import math

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
        self.nodes = [posX, negX, posY, negY, posZ, negZ]

    def update_edge(self, bearing, new_edge):
        match bearing:
            case 1:
                self.nodes[0] = new_edge
                new_edge.next.nodes[1]= Edge(self, new_edge.distance)
            case 2:
                self.nodes[1] = new_edge
                new_edge.next.nodes[0] = Edge(self, new_edge.distance)
            case 3:
                self.nodes[2] = new_edge
                new_edge.next.nodes[3] = Edge(self, new_edge.distance)
            case 4:
                self.nodes[3] = new_edge
                new_edge.next.nodes[2] = Edge(self, new_edge.distance)
            case 5:
                self.nodes[4] = new_edge
                new_edge.next.nodes[5] = Edge(self, new_edge.distance)
            case 6:
                self.nodes[5] = new_edge
                new_edge.next.nodes[4] = Edge(self, new_edge.distance)

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

def pathfind(graph, source):
    distances = {}
    for coord in graph.dict:
        node = graph.dict[coord]
        if node is source:
            current = [node, 0, False, None]
            distances[coord] = current
        else:
            
            distances[coord] = [node, -1, False, None]
    while current != None:
        current[2] = True

        for i in range(6):
            neighbor = distances[getPositionString(current[0].nodes[i].next.pos)]
            if neighbor != None and (not neighbor[2]):
                distance = current[1] + current[0].nodes[i].distance
                if neighbor[1] == -1 or neighbor[1] > distance:
                    neighbor[1] = distance
                    neighbor[3] = getPositionString(current[0].pos)

        min_dist = math.inf()
        for coord in distances:
            next_node = distances[coord]
            if next_node[1] < min_dist and (not next_node[2]):
                min_dist = distances[coord][1]
                current = next_node

    return distances

def get_path(graph, distances, start, end):
    path = []
    

        

