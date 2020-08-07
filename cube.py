from matplotlib import pyplot as plt
import numpy as np
from itertools import combinations


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

        self.net = np.array([[0.,0,0,1,1,1,0,0,0,0,0,0],
                 [0.,0,0,1,1,1,0,0,0,0,0,0],
                 [0.,0,0,1,1,1,0,0,0,0,0,0],
                 [1.,1,1,1,1,1,1,1,1,1,1,1],
                 [1.,1,1,1,1,1,1,1,1,1,1,1],
                 [1.,1,1,1,1,1,1,1,1,1,1,1],
                 [0.,0,0,1,1,1,0,0,0,0,0,0],
                 [0.,0,0,1,1,1,0,0,0,0,0,0],
                 [0.,0,0,1,1,1,0,0,0,0,0,0]])
        self.net = np.repeat(self.net[:,:,np.newaxis],3,axis=2)

        self.white = (1,1,1)
        self.yellow = (1,1,51/255)
        self.green = (0,150/255,20/255)
        self.blue = (0,102/255,204/255)
        self.red = (1,0,30/255)
        self.orange = (1,118/255,0)

        self.net[:3,3:6,:] = self.white
        self.net[6:9,3:6,:] = self.yellow
        self.net[3:6,:3,:] = self.orange
        self.net[3:6,3:6,:] = self.green
        self.net[3:6,6:9,:] = self.red
        self.net[3:6,9:12,:] = self.blue

        self.edge_coords = {
            1 : [(2,4),(3,4)],
            2 : [(1,5),(3,7)],
            3 : [(0,4),(3,10)],
            4 : [(1,3),(3,1)],
            5 : [(4,3),(4,2)],
            6 : [(4,5),(4,6)],
            7 : [(4,9),(4,8)],
            8 : [(4,11),(4,0)],
            9 : [(6,4),(5,4)],
            10 : [(7,5),(5,7)],
            11 : [(8,4),(5,10)],
            12 : [(7,3),(5,1)]
        }

        self.corner_coords = {
            1 : [(2,3),(3,3),(3,2)],
            2 : [(2,5),(3,6),(3,5)],
            3 : [(0,5),(3,9),(3,8)],
            4 : [(0,3),(3,0),(3,11)],
            5 : [(6,3),(5,2),(5,3)],
            6 : [(6,5),(5,5),(5,6)],
            7 : [(8,5),(5,8),(5,9)],
            8 : [(8,3),(5,11),(5,0)],
        }
        self.render()


    def solve(self):
        self.__init__()

    def scramble(self):
        choices = ['F','B','R','L','U','D','F2','B2','R2','L2','U2','D2',"F'","B'","R'","L'","U'","D'",]
        command = ''
        for i in range(21):
            command += choices[np.random.randint(0,18)]
            command += ' '
        self.move(command)

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
            if letter.upper() == "U2" or letter.upper() == "U'2":
                self.move_("U")
                self.move_("U")
            elif letter.upper() == "D2" or letter.upper() == "D'2":
                self.move_("D")
                self.move_("D")
            if letter.upper() == "F2" or letter.upper() == "F'2":
                self.move_("F")
                self.move_("F")
            if letter.upper() == "B2" or letter.upper() == "B'2":
                self.move_("B")
                self.move_("B")
            if letter.upper() == "R2" or letter.upper() == "R'2":
                self.move_("R")
                self.move_("R")
            if letter.upper() == "L2" or letter.upper() == "L'2":
                self.move_("L")
                self.move_("L")
            else:
                self.move_(letter)
        self.render()

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

    def key2color(self,key):
        if key == 'w':
            return self.white
        elif key == 'y':
            return self.yellow
        elif key == 'g':
            return self.green
        elif key == 'b':
            return self.blue
        elif key == 'r':
            return self.red
        elif key == 'o':
            return self.orange
        else:
            raise ValueError("Invalid key")

    def render(self):
        for i in range(1,9):
            orientation = self.corners[i].orientation
            xy1,xy2,xy3 = self.corner_coords[self.corners[i].position]
            color1, color2, color3 = self.corners[i].colors
            if orientation == 2: # needs to rotate ccw
                color1 = self.key2color(color1)
                color2 = self.key2color(color2)
                color3 = self.key2color(color3)
                x1,y1 = xy1
                x2,y2 = xy2
                x3,y3 = xy3
                self.net[x1,y1,:] = color3
                self.net[x2,y2,:] = color1
                self.net[x3,y3,:] = color2
            elif orientation == 1: # needs to rotate cw
                color1 = self.key2color(color1)
                color2 = self.key2color(color2)
                color3 = self.key2color(color3)
                x1,y1 = xy1
                x2,y2 = xy2
                x3,y3 = xy3
                self.net[x1,y1,:] = color2
                self.net[x2,y2,:] = color3
                self.net[x3,y3,:] = color1
            else: # orientation == 0: # oriented properly
                color1 = self.key2color(color1)
                color2 = self.key2color(color2)
                color3 = self.key2color(color3)
                x1,y1 = xy1
                x2,y2 = xy2
                x3,y3 = xy3
                self.net[x1,y1,:] = color1
                self.net[x2,y2,:] = color2
                self.net[x3,y3,:] = color3

        for i in range(1,13): # an oriented middle edge is g/b touching w/y/g/b
        # a disoriented medge is o/r touching w/y
        # an oriented tedge w/y touching b/g
        # a disoriented tedge is w/y not touching w/y   or   w/y touching o/r
            disoriented = self.edges[i].orientation
            xy1,xy2 = self.edge_coords[self.edges[i].position]
            color1, color2 = self.edges[i].colors
            if color1 == 'y' or color1 == 'w':
                if not disoriented:
                    color1 = self.key2color(color1)
                    color2 = self.key2color(color2)
                    x1,y1 = xy1
                    x2,y2 = xy2
                    self.net[x1,y1,:] = color1
                    self.net[x2,y2,:] = color2
                else: # w/y needs to be on g or b
                    color1 = self.key2color(color1)
                    color2 = self.key2color(color2)
                    x1,y1 = xy1
                    x2,y2 = xy2
                    self.net[x1,y1,:] = color2  # ordering switched
                    self.net[x2,y2,:] = color1
            else: # it's a middle edge with color1 = 'g' or 'b'
                if not disoriented:
                    color1 = self.key2color(color1)
                    color2 = self.key2color(color2)
                    x1,y1 = xy1
                    x2,y2 = xy2
                    self.net[x1,y1,:] = color1
                    self.net[x2,y2,:] = color2
                else:
                    color1 = self.key2color(color1)
                    color2 = self.key2color(color2)
                    x1,y1 = xy1
                    x2,y2 = xy2
                    self.net[x1,y1,:] = color2 # ordering switched
                    self.net[x2,y2,:] = color1


        plt.xticks([])
        plt.yticks([])
        plt.imshow(self.net)
        plt.show()



class Cubie():
    def __init__(self):
        self.type = None
        self.corner_colors = {
            1 : ['w','g','o'],
            2 : ['w','r','g'],
            3 : ['w','b','r'],
            4 : ['w','o','b'],
            5 : ['y','o','g'],
            6 : ['y','g','r'],
            7 : ['y','r','b'],
            8 : ['y','b','o']
        }
        self.edge_colors = {
            1 : ['w','g'],
            2 : ['w','r'],
            3 : ['w','b'],
            4 : ['w','o'],

            5 : ['g','o'],
            6 : ['g','r'],
            7 : ['b','r'],
            8 : ['b','o'],

            9 : ['y','g'],
            10 : ['y','r'],
            11 : ['y','b'],
            12 : ['y','o']
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
