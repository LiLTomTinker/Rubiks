from itertools import permutations
import numpy as np


class Cube():
    def __init__(self):
        self.corners = {i : Corner(i) for i in range(1,9)}
        self.edges = {i : Edge(i) for i in range(1,13)}
        self.centers = {i : Center(i) for i in range(1,7)}

        # the edges are a list of the indices of the edges currently in the slots ORDER MATTERS
        self.top = {'edges':[1,2,3,4], 'corners':[1,2,3,4], 'center':1}
        self.down = {'edges':[9,10,11,12],'corners':[5,6,7,8], 'center':6}
        self.front = {'edges':[1,5,6,9],'corners':[1,2,5,6], 'center':2}
        self.back = {'edges':[3,7,8,11],'corners':[3,4,7,8], 'center':4}
        self.left = {'edges':[4,5,8,12],'corners':[1,4,5,8], 'center':5}
        self.right = {'edges':[2,6,7,10],'corners':[2,3,6,7], 'center':3}
        self.middle_x = {'edges':[5,6,7,8],'centers':[2,3,4,5]}
        self.middle_y = {'edges':[1,3,9,11],'centers':[1,2,4,6]}
        self.middle_z = {'edges':[2,4,10,12],'centers':[1,3,5,6]}

    def solve(self):
        pass

    def scramble(self):
        pass

    def is_solved(self):
        oriented = 0
        for i in range(1,9):
            oriented += self.corners[i].orientation
            if self.corners[i].position != self.corners[i].label:
                return False
        for i in range(1,13):
            oriented += self.edges[i].orientation
            if self.edges[i].position != self.edges[i].label:
                return False
        return oriented == 0


    def update_positions(self):
        #update across top, middle, and bottom
        for i,e in enumerate(self.top['edges']):
            self.edges[e].position = i+1
        for i,c in enumerate(self.top['corners']):
            self.corners[c].position = i+1
        self.edges[self.front['edges'][1]].position = 5
        self.edges[self.front['edges'][2]].position = 6
        self.edges[self.back['edges'][1]].position = 7
        self.edges[self.back['edges'][2]].position = 8
        for i,e in enumerate(self.down['edges']):
            self.edges[e].position = i+9
        for i,c in enumerate(self.down['corners']):
            self.corners[c].position = i+5

    def permute(self,x,permutation):
        # permute(x,[1,2,3,0])
        # 0 --> 1
        # 1 --> 2
        # 2 --> 3
        # 3 --> 0
        # the permutation is the outcome, by indices
        y = x.copy()
        for i in range(len(x)):
            x[i] = y[permutation[i]]
        return x

    def move(self, command):
        command = command.split()
        for letter in command:
            self.move_(letter)

    def move_(self,command):
        # a single letter (or letter prime) move
        command = command.upper()

        if command == "U":
            self.permute(self.top['edges'],[1,2,3,0])
            self.permute(self.top['corners'],[1,2,3,0])
            self.front['edges'][0] = self.top['edges'][0]
            self.right['edges'][0] = self.top['edges'][1]
            self.back['edges'][0] = self.top['edges'][2]
            self.left['edges'][0] = self.top['edges'][3]
            self.front['corners'][0] = self.top['corners'][0]
            self.front['corners'][1] = self.top['corners'][1]
            self.right['corners'][0] = self.top['corners'][1]
            self.right['corners'][1] = self.top['corners'][2]
            self.back['corners'][0] = self.top['corners'][2]
            self.back['corners'][1] = self.top['corners'][3]
            self.left['corners'][0] = self.top['corners'][0]
            self.left['corners'][1] = self.top['corners'][3]
            self.update_positions()

        elif command == "U'":
            self.permute(self.top['edges'],[3,0,1,2])
            self.permute(self.top['corners'],[3,0,1,2])
            self.front['edges'][0] = self.top['edges'][0]
            self.right['edges'][0] = self.top['edges'][1]
            self.back['edges'][0] = self.top['edges'][2]
            self.left['edges'][0] = self.top['edges'][3]
            self.front['corners'][0] = self.top['corners'][0]
            self.front['corners'][1] = self.top['corners'][1]
            self.right['corners'][0] = self.top['corners'][1]
            self.right['corners'][1] = self.top['corners'][2]
            self.back['corners'][0] = self.top['corners'][2]
            self.back['corners'][1] = self.top['corners'][3]
            self.left['corners'][0] = self.top['corners'][0]
            self.left['corners'][1] = self.top['corners'][3]
            self.update_positions()

        elif command == "D":
            self.permute(self.down['edges'],[3,0,1,2])
            self.permute(self.down['corners'],[3,0,1,2])
            self.front['edges'][3] = self.down['edges'][0]
            self.right['edges'][3] = self.down['edges'][1]
            self.back['edges'][3] = self.down['edges'][2]
            self.left['edges'][3] = self.down['edges'][3]
            self.front['corners'][2] = self.down['corners'][0]
            self.front['corners'][3] = self.down['corners'][1]
            self.right['corners'][2] = self.down['corners'][1]
            self.right['corners'][3] = self.down['corners'][2]
            self.back['corners'][2] = self.down['corners'][2]
            self.back['corners'][3] = self.down['corners'][3]
            self.left['corners'][2] = self.down['corners'][0]
            self.left['corners'][3] = self.down['corners'][3]
            self.update_positions()

        elif command == "D'":
            self.permute(self.down['edges'],[1,2,3,0]) # reversed perspective
            self.permute(self.down['corners'],[1,2,3,0])
            self.front['edges'][3] = self.down['edges'][0]
            self.right['edges'][3] = self.down['edges'][1]
            self.back['edges'][3] = self.down['edges'][2]
            self.left['edges'][3] = self.down['edges'][3]
            self.front['corners'][2] = self.down['corners'][0]
            self.front['corners'][3] = self.down['corners'][1]
            self.right['corners'][2] = self.down['corners'][1]
            self.right['corners'][3] = self.down['corners'][2]
            self.back['corners'][2] = self.down['corners'][2]
            self.back['corners'][3] = self.down['corners'][3]
            self.left['corners'][2] = self.down['corners'][0]
            self.left['corners'][3] = self.down['corners'][3]
            self.update_positions()

        elif command == "F":
            # Update orientations
            for i in range(4):
                self.edges[self.front['edges'][i]].orientation = (self.edges[self.front['edges'][i]].orientation + 1) % 2
            self.corners[self.front['corners'][0]].orientation = (self.corners[self.front['corners'][0]].orientation + 2) % 3
            self.corners[self.front['corners'][1]].orientation = (self.corners[self.front['corners'][1]].orientation + 1) % 3
            self.corners[self.front['corners'][2]].orientation = (self.corners[self.front['corners'][2]].orientation + 1) % 3
            self.corners[self.front['corners'][3]].orientation = (self.corners[self.front['corners'][3]].orientation + 2) % 3

            self.permute(self.front['edges'],[1,3,0,2])
            self.permute(self.front['corners'],[2,0,3,1])

            self.top['edges'][0] = self.front['edges'][0]
            self.right['edges'][1] = self.front['edges'][2]
            self.left['edges'][1] = self.front['edges'][1]
            self.down['edges'][0] = self.front['edges'][3]

            self.top['corners'][0] = self.front['corners'][0]
            self.top['corners'][1] = self.front['corners'][1]
            self.right['corners'][0] = self.front['corners'][1]
            self.right['corners'][2] = self.front['corners'][3]
            self.down['corners'][0] = self.front['corners'][2]
            self.down['corners'][1] = self.front['corners'][3]
            self.left['corners'][0] = self.front['corners'][0]
            self.left['corners'][2] = self.front['corners'][2]
            self.update_positions()

        elif command == "F'":
            # Update orientations of corners and edges
            for i in range(4):
                self.edges[self.front['edges'][i]].orientation = (self.edges[self.front['edges'][i]].orientation + 1) % 2
            self.corners[self.front['corners'][0]].orientation = (self.corners[self.front['corners'][0]].orientation + 2) % 3
            self.corners[self.front['corners'][1]].orientation = (self.corners[self.front['corners'][1]].orientation + 1) % 3
            self.corners[self.front['corners'][2]].orientation = (self.corners[self.front['corners'][2]].orientation + 1) % 3
            self.corners[self.front['corners'][3]].orientation = (self.corners[self.front['corners'][3]].orientation + 2) % 3

            self.permute(self.front['edges'],[2,0,3,1])
            self.permute(self.front['corners'],[1,3,0,2])

            self.top['edges'][0] = self.front['edges'][0]
            self.right['edges'][1] = self.front['edges'][2]
            self.left['edges'][1] = self.front['edges'][1]
            self.down['edges'][0] = self.front['edges'][3]

            self.top['corners'][0] = self.front['corners'][0]
            self.top['corners'][1] = self.front['corners'][1]
            self.right['corners'][0] = self.front['corners'][1]
            self.right['corners'][2] = self.front['corners'][3]
            self.down['corners'][0] = self.front['corners'][2]
            self.down['corners'][1] = self.front['corners'][3]
            self.left['corners'][0] = self.front['corners'][0]
            self.left['corners'][2] = self.front['corners'][2]
            self.update_positions()

        elif command == "R":
            # Update orientations of corners only
            self.corners[self.right['corners'][0]].orientation = (self.corners[self.right['corners'][0]].orientation + 2) % 3
            self.corners[self.right['corners'][1]].orientation = (self.corners[self.right['corners'][1]].orientation + 1) % 3
            self.corners[self.right['corners'][2]].orientation = (self.corners[self.right['corners'][2]].orientation + 1) % 3
            self.corners[self.right['corners'][3]].orientation = (self.corners[self.right['corners'][3]].orientation + 2) % 3

            self.permute(self.right['edges'],[1,3,0,2])
            self.permute(self.right['corners'],[2,0,3,1])

            self.top['edges'][1] = self.right['edges'][0]
            self.front['edges'][2] = self.right['edges'][1]
            self.back['edges'][1] = self.right['edges'][2]
            self.down['edges'][1] = self.right['edges'][3]

            self.top['corners'][1] = self.right['corners'][0]
            self.top['corners'][2] = self.right['corners'][1]
            self.front['corners'][1] = self.right['corners'][0]
            self.front['corners'][3] = self.right['corners'][2]
            self.down['corners'][1] = self.right['corners'][2]
            self.down['corners'][2] = self.right['corners'][3]
            self.back['corners'][0] = self.right['corners'][1]
            self.back['corners'][2] = self.right['corners'][3]
            self.update_positions()

        elif command == "R'":
            # Update orientations of corners only
            self.corners[self.right['corners'][0]].orientation = (self.corners[self.right['corners'][0]].orientation + 2) % 3
            self.corners[self.right['corners'][1]].orientation = (self.corners[self.right['corners'][1]].orientation + 1) % 3
            self.corners[self.right['corners'][2]].orientation = (self.corners[self.right['corners'][2]].orientation + 1) % 3
            self.corners[self.right['corners'][3]].orientation = (self.corners[self.right['corners'][3]].orientation + 2) % 3

            self.permute(self.right['edges'],[2,0,3,1])
            self.permute(self.right['corners'],[1,3,0,2])

            self.top['edges'][1] = self.right['edges'][0]
            self.front['edges'][2] = self.right['edges'][1]
            self.back['edges'][1] = self.right['edges'][2]
            self.down['edges'][1] = self.right['edges'][3]

            self.top['corners'][1] = self.right['corners'][0]
            self.top['corners'][2] = self.right['corners'][1]
            self.front['corners'][1] = self.right['corners'][0]
            self.front['corners'][3] = self.right['corners'][2]
            self.down['corners'][1] = self.right['corners'][2]
            self.down['corners'][2] = self.right['corners'][3]
            self.back['corners'][0] = self.right['corners'][1]
            self.back['corners'][2] = self.right['corners'][3]
            self.update_positions()

        elif command == "B":
            # Update orientations
            for i in range(4):
                self.edges[self.back['edges'][i]].orientation = (self.edges[self.back['edges'][i]].orientation + 1) % 2
            self.corners[self.back['corners'][0]].orientation = (self.corners[self.back['corners'][0]].orientation + 2) % 3
            self.corners[self.back['corners'][1]].orientation = (self.corners[self.back['corners'][1]].orientation + 1) % 3
            self.corners[self.back['corners'][2]].orientation = (self.corners[self.back['corners'][2]].orientation + 1) % 3
            self.corners[self.back['corners'][3]].orientation = (self.corners[self.back['corners'][3]].orientation + 2) % 3

            self.permute(self.back['edges'],[1,3,0,2])
            self.permute(self.back['corners'],[2,0,3,1])

            self.top['edges'][2] = self.back['edges'][0]
            self.right['edges'][2] = self.back['edges'][1]
            self.left['edges'][2] = self.back['edges'][2]
            self.down['edges'][2] = self.back['edges'][3]

            self.top['corners'][2] = self.back['corners'][0]
            self.top['corners'][3] = self.back['corners'][1]
            self.right['corners'][1] = self.back['corners'][0]
            self.right['corners'][3] = self.back['corners'][2]
            self.down['corners'][2] = self.back['corners'][2]
            self.down['corners'][3] = self.back['corners'][3]
            self.left['corners'][1] = self.back['corners'][1]
            self.left['corners'][3] = self.back['corners'][3]
            self.update_positions()

        elif command == "B'":
            # Update orientations
            for i in range(4):
                self.edges[self.back['edges'][i]].orientation = (self.edges[self.back['edges'][i]].orientation + 1) % 2
            self.corners[self.back['corners'][0]].orientation = (self.corners[self.back['corners'][0]].orientation + 2) % 3
            self.corners[self.back['corners'][1]].orientation = (self.corners[self.back['corners'][1]].orientation + 1) % 3
            self.corners[self.back['corners'][2]].orientation = (self.corners[self.back['corners'][2]].orientation + 1) % 3
            self.corners[self.back['corners'][3]].orientation = (self.corners[self.back['corners'][3]].orientation + 2) % 3

            self.permute(self.back['edges'],[2,0,3,1])
            self.permute(self.back['corners'],[1,3,0,2])

            self.top['edges'][2] = self.back['edges'][0]
            self.right['edges'][2] = self.back['edges'][1]
            self.left['edges'][2] = self.back['edges'][2]
            self.down['edges'][2] = self.back['edges'][3]

            self.top['corners'][2] = self.back['corners'][0]
            self.top['corners'][3] = self.back['corners'][1]
            self.right['corners'][1] = self.back['corners'][0]
            self.right['corners'][3] = self.back['corners'][2]
            self.down['corners'][2] = self.back['corners'][2]
            self.down['corners'][3] = self.back['corners'][3]
            self.left['corners'][1] = self.back['corners'][1]
            self.left['corners'][3] = self.back['corners'][3]
            self.update_positions()

        elif command == "L":
            # Update orientations of corners only
            self.corners[self.left['corners'][0]].orientation = (self.corners[self.left['corners'][0]].orientation + 1) % 3
            self.corners[self.left['corners'][1]].orientation = (self.corners[self.left['corners'][1]].orientation + 2) % 3
            self.corners[self.left['corners'][2]].orientation = (self.corners[self.left['corners'][2]].orientation + 2) % 3
            self.corners[self.left['corners'][3]].orientation = (self.corners[self.left['corners'][3]].orientation + 1) % 3

            self.permute(self.left['edges'],[2,0,3,1])
            self.permute(self.left['corners'],[1,3,0,2])

            self.top['edges'][3] = self.left['edges'][0]
            self.front['edges'][1] = self.left['edges'][1]
            self.back['edges'][2] = self.left['edges'][2]
            self.down['edges'][3] = self.left['edges'][3]

            self.top['corners'][0] = self.left['corners'][0]
            self.top['corners'][3] = self.left['corners'][1]
            self.front['corners'][0] = self.left['corners'][0]
            self.front['corners'][2] = self.left['corners'][2]
            self.down['corners'][0] = self.left['corners'][2]
            self.down['corners'][3] = self.left['corners'][3]
            self.back['corners'][1] = self.left['corners'][1]
            self.back['corners'][3] = self.left['corners'][3]
            self.update_positions()

        elif command == "L'":
            # Update orientations of corners only
            self.corners[self.left['corners'][0]].orientation = (self.corners[self.left['corners'][0]].orientation + 1) % 3
            self.corners[self.left['corners'][1]].orientation = (self.corners[self.left['corners'][1]].orientation + 2) % 3
            self.corners[self.left['corners'][2]].orientation = (self.corners[self.left['corners'][2]].orientation + 2) % 3
            self.corners[self.left['corners'][3]].orientation = (self.corners[self.left['corners'][3]].orientation + 1) % 3

            self.permute(self.left['edges'],[1,3,0,2])
            self.permute(self.left['corners'],[2,0,3,1])

            self.top['edges'][3] = self.left['edges'][0]
            self.front['edges'][1] = self.left['edges'][1]
            self.back['edges'][2] = self.left['edges'][2]
            self.down['edges'][3] = self.left['edges'][3]

            self.top['corners'][0] = self.left['corners'][0]
            self.top['corners'][3] = self.left['corners'][1]
            self.front['corners'][0] = self.left['corners'][0]
            self.front['corners'][2] = self.left['corners'][2]
            self.down['corners'][0] = self.left['corners'][2]
            self.down['corners'][3] = self.left['corners'][3]
            self.back['corners'][1] = self.left['corners'][1]
            self.back['corners'][3] = self.left['corners'][3]
            self.update_positions()

    def view(self):
        print("TOP: (" + self.centers[self.top['center']].color + ")",self.top,'\n',
              "BOTTOM: (" + self.centers[self.down['center']].color + ")",self.down,'\n',
              "FRONT: (" + self.centers[self.front['center']].color + ")",self.front,'\n',
              "BACK: (" + self.centers[self.back['center']].color + ")",self.back,'\n',
              "LEFT: (" + self.centers[self.left['center']].color + ")",self.left,'\n',
              "RIGHT: (" + self.centers[self.right['center']].color + ")",self.right)




class Cubie():
    def __init__(self):
        self.type = None
        self.corner_colors = {
            1 : ['w','o','g'],
            2 : ['w','g','r'],
            3 : ['w','r','b'],
            4 : ['w','b','o'],
            5 : ['y','g','o'],
            6 : ['y','r','g'],
            7 : ['y','b','r'],
            8 : ['y','o','b']
        }
        self.edge_colors = {
            1 : ['w','g'],
            2 : ['w','r'],
            3 : ['w','b'],
            4 : ['w','o'],

            5 : ['o','g'],
            6 : ['g','r'],
            7 : ['r','b'],
            8 : ['b','o'],

            9 : ['g','y'],
            10 : ['r','y'],
            11 : ['b','y'],
            12 : ['o','y']
        }
        self.center_colors = {
            1 : 'w',
            2 : 'g',
            3 : 'r',
            4 : 'b',
            5 : 'o',
            6 : 'y',
        }
    def about(self):
        print("COLORS:",self.colors,'\n',
              "ORIENTATION:",self.orientation,'\n',
              "POSITION:",self.position)

class Corner(Cubie):
    def __init__(self, corner_index):
        super(Corner, self).__init__()
        self.colors = self.corner_colors[corner_index]
        self.orientation = 0 # could also be 1 or 2
        self.label = corner_index
        self.type = 'corner'
        self.position = corner_index



class Edge(Cubie):
    def __init__(self, edge_index):
        super(Edge, self).__init__()
        self.colors = self.edge_colors[edge_index]
        self.orientation = 0 # correctly oriented
        self.label = edge_index
        self.type = 'edge'
        self.position = edge_index


class Center(Cubie):
    def __init__(self, center_index):
        super(Center, self).__init__()
        self.color = self.center_colors[center_index]
        self.label = center_index
        self.type = 'center'
        #self.orientation = 0
