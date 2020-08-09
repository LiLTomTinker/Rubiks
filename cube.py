from matplotlib import pyplot as plt
import numpy as np
import pickle

class Cube():
    def __init__(self):
        plt.ion() # interactive plotting
        self.corners = {i : Corner(i) for i in range(1,9)}
        self.edges = {i : Edge(i) for i in range(1,13)}
        self.centers = {i : Center(i) for i in range(1,7)}

        self.aligned_x = 1
        self.aligned_y = 1
        self.aligned_z = 1

        # the edges are a list of the indices of the edges currently in the slots ORDER MATTERS
        self.top = {'edges':[1,2,3,4], 'corners':[1,2,3,4], 'center':1}
        self.middle = {'edges': [5,6,7,8], 'centers': [2,3,4,5]}
        self.bottom = {'edges':[9,10,11,12],'corners':[5,6,7,8], 'center':6}

        # Working on refactoring and removing this unnecessary code
        # self.front = {'edges':[1,5,6,9],'corners':[1,2,5,6], 'center':2}
        # self.back = {'edges':[3,7,8,11],'corners':[3,4,7,8], 'center':4}
        # self.left = {'edges':[4,5,8,12],'corners':[1,4,5,8], 'center':5}
        # self.right = {'edges':[2,6,7,10],'corners':[2,3,6,7], 'center':3}
        # self.middle_y = {'edges':[1,3,9,11],'centers':[1,2,4,6]}
        # self.middle_z = {'edges':[2,4,10,12],'centers':[1,3,5,6]}

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
        self.yellow = (1,1,31/255)
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

        self.center_coords = {
            1 : (1,4),
            2 : (4,4),
            3 : (4,7),
            4 : (4,10),
            5 : (4,1),
            6 : (7,4)
        }

        self.render()

        self.undo_cache = []
        self.undo_counter = -1

    def primed(self,command):
        primed_command = ''
        for letter in command.split()[::-1]:
            if "'" in letter:
                letter = letter[:-1]
            else:
                letter += "'"
            primed_command += letter
            primed_command += " "

        return primed_command

    def undo(self):
        if len(self.undo_cache) == 0 or -self.undo_counter > len(self.undo_cache):
            print("Nothing to undo")
        else:
            undo_command = self.undo_cache[self.undo_counter]
            self.undo_counter -= 1
            cube.move(self.primed(undo_command), cache=False)
            print("Undo",undo_command)
    def redo(self):
        if self.undo_counter == -1:
            print("Nothing to redo")
        else:
            command = self.undo_cache[self.undo_counter + 1]
            cube.move(command, cache=False)
            self.undo_counter += 1
            print("Redo",command)
    def solve(self):
        self.__init__()

    def scramble(self):
        choices = ['F','B','R','L','U','D','F2','B2','R2','L2','U2','D2',"F'","B'","R'","L'","U'","D'","M","E","S","M2","E2","S2"]
        command = ''
        for i in range(28):
            command += choices[np.random.randint(0,21)]
            command += ' '
        self.move(command)
        print(command)

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
        self.centers[self.top['center']].position = 1

        for i,e in enumerate(self.middle['edges']):
            self.edges[e].position = i+5
        for i,c in enumerate(self.middle['centers']):
            self.centers[c].position = i+2

        for i,e in enumerate(self.bottom['edges']):
            self.edges[e].position = i+9
        for i,c in enumerate(self.bottom['corners']):
            self.corners[c].position = i+5
        self.centers[self.bottom['center']].position = 6

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

    def move(self, command, cache=True):
        command = command.replace("[",'').replace("]",'').replace("xy","x y")
        command = command.replace("xz","x z").replace("yx","y x").replace("yz","y z")
        command = command.replace("zx","z x").replace("zy","z y").replace("(",'').replace(")",'')
        if cache:
            if self.undo_counter != -1:
                self.undo_cache = self.undo_cache[:self.undo_counter+1]
                self.undo_counter = -1
            self.undo_cache.append(command)
        command = command.split()
        for letter in command:
            if letter.upper() in ["U2","U2'"]:
                self.move_("U")
                self.move_("U")
            elif letter.upper() in ["D2","D2'"]:
                self.move_("D")
                self.move_("D")
            elif letter.upper() in ["F2","F2'"]:
                self.move_("F")
                self.move_("F")
            elif letter.upper() in ["B2","B2'"]:
                self.move_("B")
                self.move_("B")
            elif letter.upper() in ["R2","R2'"]:
                self.move_("R")
                self.move_("R")
            elif letter.upper() in ["L2","L2'"]:
                self.move_("L")
                self.move_("L")
            elif letter.upper() == "R'":
                self.move_("R")
                self.move_("R")
                self.move_("R")
            elif letter.upper() == "L'":
                self.move_("L")
                self.move_("L")
                self.move_("L")
            elif letter.upper() == "F'":
                self.move_("F")
                self.move_("F")
                self.move_("F")
            elif letter.upper() == "B'":
                self.move_("B")
                self.move_("B")
                self.move_("B")
            elif letter.upper() == "U'":
                self.move_("U")
                self.move_("U")
                self.move_("U")
            elif letter.upper() == "D'":
                self.move_("D")
                self.move_("D")
                self.move_("D")
            elif letter.upper() in ["X","[X]"]:
                self.move_("L")
                self.move_("L")
                self.move_("L")
                self.move_("R")
                self.move_("M")
                self.move_("M")
                self.move_("M")
            elif letter.upper() in ["X'","[X']"]:
                self.move_("L")
                self.move_("R")
                self.move_("R")
                self.move_("R")
                self.move_("M")
            elif letter.upper() in ["X2","X2'","[X2]","[X2']"]:
                self.move_("L")
                self.move_("R")
                self.move_("M")
                self.move_("L")
                self.move_("R")
                self.move_("M")
            elif letter.upper() == "M'":
                self.move_("M")
                self.move_("M")
                self.move_("M")
            elif letter.upper() in ["M2","M2'"]:
                self.move_("M")
                self.move_("M")
            elif letter.upper() in ["E2","E2'"]:
                self.move_("E")
                self.move_("E")
            elif letter.upper() == "E'":
                self.move_("E")
                self.move_("E")
                self.move_("E")
            elif letter.upper() in ["Y","[Y]"]:
                self.move_("E")
                self.move_("E")
                self.move_("E")
                self.move_("U")
                self.move_("D")
                self.move_("D")
                self.move_("D")
            elif letter.upper() in ["Y'","[Y']"]:
                self.move_("E")
                self.move_("U")
                self.move_("U")
                self.move_("U")
                self.move_("D")
            elif letter.upper() in ["Y2","[Y2]","Y2'","[Y2']"]:
                self.move_("E")
                self.move_("U")
                self.move_("D")
                self.move_("E")
                self.move_("U")
                self.move_("D")
            elif letter.upper() == "S'":
                self.move_("S")
                self.move_("S")
                self.move_("S")
            elif letter.upper() in ["S2","S2'"]:
                self.move_("S")
                self.move_("S")
            elif letter.upper() in ["Z","[Z]"]:
                self.move_("S")
                self.move_("F")
                self.move_("B")
                self.move_("B")
                self.move_("B")
            elif letter.upper() in ["Z'","[Z']"]:
                self.move_("S")
                self.move_("S")
                self.move_("S")
                self.move_("F")
                self.move_("F")
                self.move_("F")
                self.move_("B")
            elif letter.upper() in ["Z2","[Z2]","Z2'","[Z2']"]:
                self.move_("S")
                self.move_("F")
                self.move_("B")
                self.move_("S")
                self.move_("F")
                self.move_("B")
            elif letter.upper() == "FW":
                self.move_("F")
                self.move_("S")
            elif letter.upper() == "FW'":
                self.move_("F")
                self.move_("F")
                self.move_("F")
                self.move_("S")
                self.move_("S")
                self.move_("S")
            elif letter.upper() in ["FW2","FW2'"]:
                self.move_("F")
                self.move_("S")
                self.move_("F")
                self.move_("S")
            elif letter.upper() == "BW":
                self.move_("B")
                self.move_("S")
                self.move_("S")
                self.move_("S")
            elif letter.upper() == "BW'":
                self.move_("B")
                self.move_("B")
                self.move_("B")
                self.move_("S")
            elif letter.upper() in ["BW2","BW2'"]:
                self.move_("B")
                self.move_("S")
                self.move_("B")
                self.move_("S")
            elif letter.upper() == "RW":
                self.move_("R")
                self.move_("M")
                self.move_("M")
                self.move_("M")
            elif letter.upper() == "RW'":
                self.move_("R")
                self.move_("R")
                self.move_("R")
                self.move_("M")
            elif letter.upper() in ["RW2","RW2'"]:
                self.move_("R")
                self.move_("M")
                self.move_("R")
                self.move_("M")
            elif letter.upper() == "LW":
                self.move_("L")
                self.move_("M")
            elif letter.upper() == "LW'":
                self.move_("L")
                self.move_("L")
                self.move_("L")
                self.move_("M")
                self.move_("M")
                self.move_("M")
            elif letter.upper() in ["LW2","LW2'"]:
                self.move_("L")
                self.move_("M")
                self.move_("L")
                self.move_("M")
            elif letter.upper() == "UW":
                self.move_("U")
                self.move_("E")
                self.move_("E")
                self.move_("E")
            elif letter.upper() == "UW'":
                self.move_("U")
                self.move_("U")
                self.move_("U")
                self.move_("E")
            elif letter.upper() in ["UW2","UW2'"]:
                self.move_("U")
                self.move_("E")
                self.move_("U")
                self.move_("E")
            elif letter.upper() == "DW":
                self.move_("D")
                self.move_("E")
            elif letter.upper() == "DW'":
                self.move_("D")
                self.move_("D")
                self.move_("D")
                self.move_("E")
                self.move_("E")
                self.move_("E")
            elif letter.upper() in ["DW2","DW2'"]:
                self.move_("D")
                self.move_("E")
                self.move_("D")
                self.move_("E")
            else:
                self.move_(letter)
        self.render()

    def move_(self,command):
        # a single letter (or letter prime) move
        command = command.upper()

        if command == "U":
            self.permute(self.top['edges'],[1,2,3,0])
            self.permute(self.top['corners'],[1,2,3,0])
            self.update_positions()

        elif command == "D":
            self.permute(self.bottom['edges'],[3,0,1,2])
            self.permute(self.bottom['corners'],[3,0,1,2])
            self.update_positions()

        elif command == "F":
            # Update orientation of edges
            self.edges[self.top['edges'][0]].orientation = (self.edges[self.top['edges'][0]].orientation + 1) % 2
            self.edges[self.middle['edges'][0]].orientation = (self.edges[self.middle['edges'][0]].orientation + 1) % 2
            self.edges[self.middle['edges'][1]].orientation = (self.edges[self.middle['edges'][1]].orientation + 1) % 2
            self.edges[self.bottom['edges'][0]].orientation = (self.edges[self.bottom['edges'][0]].orientation + 1) % 2

            # Update orientation of corners
            self.corners[self.top['corners'][0]].orientation = (self.corners[self.top['corners'][0]].orientation + 2) % 3
            self.corners[self.top['corners'][1]].orientation = (self.corners[self.top['corners'][1]].orientation + 1) % 3
            self.corners[self.bottom['corners'][0]].orientation = (self.corners[self.bottom['corners'][0]].orientation + 1) % 3
            self.corners[self.bottom['corners'][1]].orientation = (self.corners[self.bottom['corners'][1]].orientation + 2) % 3

            # Permute edges
            temp = self.top['edges'][0]
            self.top['edges'][0] = self.middle['edges'][0]
            self.middle['edges'][0] = self.bottom['edges'][0]
            self.bottom['edges'][0] = self.middle['edges'][1]
            self.middle['edges'][1] = temp

            # Permute corners
            temp = self.top['corners'][0]
            self.top['corners'][0] = self.bottom['corners'][0]
            self.bottom['corners'][0] = self.bottom['corners'][1]
            self.bottom['corners'][1] = self.top['corners'][1]
            self.top['corners'][1] = temp

            self.update_positions()

        elif command == "R":
            # Update orientation of corners only
            self.corners[self.top['corners'][1]].orientation = (self.corners[
                                                                    self.top['corners'][1]].orientation + 2) % 3
            self.corners[self.top['corners'][2]].orientation = (self.corners[
                                                                    self.top['corners'][2]].orientation + 1) % 3
            self.corners[self.bottom['corners'][1]].orientation = (self.corners[
                                                                       self.bottom['corners'][1]].orientation + 1) % 3
            self.corners[self.bottom['corners'][2]].orientation = (self.corners[
                                                                       self.bottom['corners'][2]].orientation + 2) % 3

            # Permute edges
            temp = self.top['edges'][1]
            self.top['edges'][1] = self.middle['edges'][1]
            self.middle['edges'][1] = self.bottom['edges'][1]
            self.bottom['edges'][1] = self.middle['edges'][2]
            self.middle['edges'][2] = temp

            # Permute corners
            temp = self.top['corners'][1]
            self.top['corners'][1] = self.bottom['corners'][1]
            self.bottom['corners'][1] = self.bottom['corners'][2]
            self.bottom['corners'][2] = self.top['corners'][2]
            self.top['corners'][2] = temp

            self.update_positions()

        elif command == "B":
            # Update orientation of edges
            self.edges[self.top['edges'][2]].orientation = (self.edges[self.top['edges'][2]].orientation + 1) % 2
            self.edges[self.middle['edges'][2]].orientation = (self.edges[self.middle['edges'][2]].orientation + 1) % 2
            self.edges[self.middle['edges'][3]].orientation = (self.edges[self.middle['edges'][3]].orientation + 1) % 2
            self.edges[self.bottom['edges'][2]].orientation = (self.edges[self.bottom['edges'][2]].orientation + 1) % 2

            # Update orientation of corners
            self.corners[self.top['corners'][2]].orientation = (self.corners[
                                                                    self.top['corners'][2]].orientation + 2) % 3
            self.corners[self.top['corners'][3]].orientation = (self.corners[
                                                                    self.top['corners'][3]].orientation + 1) % 3
            self.corners[self.bottom['corners'][2]].orientation = (self.corners[
                                                                       self.bottom['corners'][2]].orientation + 1) % 3
            self.corners[self.bottom['corners'][3]].orientation = (self.corners[
                                                                       self.bottom['corners'][3]].orientation + 2) % 3

            # Permute edges
            temp = self.top['edges'][2]
            self.top['edges'][2] = self.middle['edges'][2]
            self.middle['edges'][2] = self.bottom['edges'][2]
            self.bottom['edges'][2] = self.middle['edges'][3]
            self.middle['edges'][3] = temp

            # Permute corners
            temp = self.top['corners'][2]
            self.top['corners'][2] = self.bottom['corners'][2]
            self.bottom['corners'][2] = self.bottom['corners'][3]
            self.bottom['corners'][3] = self.top['corners'][3]
            self.top['corners'][3] = temp

            self.update_positions()

        elif command == "L":
            # Update orientation of corners only
            self.corners[self.top['corners'][0]].orientation = (self.corners[
                                                                    self.top['corners'][0]].orientation + 1) % 3
            self.corners[self.top['corners'][3]].orientation = (self.corners[
                                                                    self.top['corners'][3]].orientation + 2) % 3
            self.corners[self.bottom['corners'][0]].orientation = (self.corners[
                                                                       self.bottom['corners'][0]].orientation + 2) % 3
            self.corners[self.bottom['corners'][3]].orientation = (self.corners[
                                                                       self.bottom['corners'][3]].orientation + 1) % 3

            # Permute edges
            temp = self.top['edges'][3]
            self.top['edges'][3] = self.middle['edges'][3]
            self.middle['edges'][3] = self.bottom['edges'][3]
            self.bottom['edges'][3] = self.middle['edges'][0]
            self.middle['edges'][0] = temp

            # Permute corners
            temp = self.top['corners'][3]
            self.top['corners'][3] = self.bottom['corners'][3]
            self.bottom['corners'][3] = self.bottom['corners'][0]
            self.bottom['corners'][0] = self.top['corners'][0]
            self.top['corners'][0] = temp

            self.update_positions()

        elif command == "M":
            # Permute centers
            temp = self.top['center']
            self.top['center'] = self.middle['centers'][2]
            self.middle['centers'][2] = self.bottom['center']
            self.bottom['center'] = self.middle['centers'][0]
            self.middle['centers'][0] = temp

            # Orient edges
            self.edges[self.top['edges'][0]].orientation = (self.edges[self.top['edges'][0]].orientation + 1) % 2
            self.edges[self.top['edges'][2]].orientation = (self.edges[self.top['edges'][2]].orientation + 1) % 2
            self.edges[self.bottom['edges'][0]].orientation = (self.edges[self.bottom['edges'][0]].orientation + 1) % 2
            self.edges[self.bottom['edges'][2]].orientation = (self.edges[self.bottom['edges'][2]].orientation + 1) % 2

            # Permute edges
            temp = self.top['edges'][0]
            self.top['edges'][0] = self.top['edges'][2]
            self.top['edges'][2] = self.bottom['edges'][2]
            self.bottom['edges'][2] = self.bottom['edges'][0]
            self.bottom['edges'][0] = temp
            self.update_positions()

        elif command == "E":
            # Permute centers
            self.permute(self.middle['centers'],[3,0,1,2])
            self.permute(self.middle['edges'],[3,0,1,2])
            # Orient edges
            self.edges[self.middle['edges'][0]].orientation = (self.edges[self.middle['edges'][0]].orientation + 1) % 2
            self.edges[self.middle['edges'][1]].orientation = (self.edges[self.middle['edges'][1]].orientation + 1) % 2
            self.edges[self.middle['edges'][2]].orientation = (self.edges[self.middle['edges'][2]].orientation + 1) % 2
            self.edges[self.middle['edges'][3]].orientation = (self.edges[self.middle['edges'][3]].orientation + 1) % 2
            # Permute edges
            self.update_positions()

        elif command == "S":
            # Permute centers
            temp = self.top['center']
            self.top['center'] = self.middle['centers'][3]
            self.middle['centers'][3] = self.bottom['center']
            self.bottom['center'] = self.middle['centers'][1]
            self.middle['centers'][1] = temp

            # Orient edges
            self.edges[self.top['edges'][3]].orientation = (self.edges[self.top['edges'][3]].orientation + 1) % 2
            self.edges[self.top['edges'][1]].orientation = (self.edges[self.top['edges'][1]].orientation + 1) % 2
            self.edges[self.bottom['edges'][1]].orientation = (self.edges[self.bottom['edges'][1]].orientation + 1) % 2
            self.edges[self.bottom['edges'][3]].orientation = (self.edges[self.bottom['edges'][3]].orientation + 1) % 2

            # Permute edges
            temp = self.top['edges'][1]
            self.top['edges'][1] = self.top['edges'][3]
            self.top['edges'][3] = self.bottom['edges'][3]
            self.bottom['edges'][3] = self.bottom['edges'][1]
            self.bottom['edges'][1] = temp
            self.update_positions()
        else:
            # Don't record the last move if it was garbage
            self.undo_cache = self.undo_cache[:-1]


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
        # Render corners
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

        # Render edges
        for i in range(1,13): # an oriented middle edge is g/b touching w/y/g/b
        # a disoriented medge is o/r touching w/y
        # an oriented tedge w/y touching b/g
        # a disoriented tedge is w/y not touching w/y   or   w/y touching o/r
            disoriented = self.edges[i].orientation
            xy1,xy2 = self.edge_coords[self.edges[i].position]
            color1, color2 = self.edges[i].colors
            if color1 == self.centers[self.top['center']].color or color1 == self.centers[self.bottom['center']].color:
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

        # Render centers
        for i in range(1,7):
            x,y = self.center_coords[self.centers[i].position]
            color = self.key2color(self.centers[i].color)
            self.net[x,y,:] = color


        plt.xticks(ticks=[i - .5 for i in np.arange(12)],labels=[])
        plt.yticks(ticks=[i - .5 for i in np.arange(9)],labels=[])
        plt.imshow(self.net)
        plt.grid(which='both',linestyle='-', linewidth='1', color='black')
        plt.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            labelbottom=False) # labels along the bottom edge are off
        plt.title("Python 2D Cube Simulator by LiLTomTinker",fontsize=7, loc='right')
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
        self.position = center_index
        #self.orientation = 0

def help():
    print("HELP:\n",
          "Input move(s) separated with a space with keyboard.\n",
          "Possible moves:\n",
          "F B R L U D M S E\n",
          "Doubles are supported (F2)\n",
          "Double slices supported (Fw, Bw)\n",
          "Primes are supported (F',U2')\n",
          "Middle slices supported (M, S, E)\n",
          "Rotate entire cube (x, y, z)\n",
          "Further commands include:\n",
          "scramble\n",
          "solve\n",
          "undo\n",
          "redo\n",
          "history\n",
          "save - save cube state\n",
          "load - load cube state\n",
          "quit or q - leave simulator\n",
          "In shell, type in 'ipython', and then '%run cube.py' to explore further")

if __name__ == "__main__":

    cube = Cube()
    print("Play with your cube! (For help: Type help)")
    key = ''
    while key != 'q':
        key = input(">> ")
        if key.strip() == "undo":
            cube.undo()
        elif key.strip() == "redo":
            cube.redo()
        elif key.strip() == "cache":
            print("Cache:",cube.undo_cache,"\nPosition:",cube.undo_counter)
        elif key.strip() == "history":
            print(cube.undo_cache)
        elif key.strip() == "solve":
            cube.solve()
        elif key.strip() == "scramble":
            cube.scramble()
        elif key.lower().strip() == "help":
            help()
        elif key.lower().strip() == "save":
            filename = input("Save cube state as: ")
            if filename == 'q':
                break
            with open(filename + '.cube', 'wb') as f:
                pickle.dump(cube, f)
            print("Saved: "+ '"' + filename + '.cube"')
        elif key.lower().strip() == "load":
            filename = input("Load cube state: ")
            if ".cube" not in filename:
                filename += '.cube'
            try:
                with open(filename,'rb') as f:
                    cube = pickle.load(f)
                    cube.render()
                    print("Loaded: "+'"'+filename+'"')
            except OSError as e:
                print(e)
        elif key.strip() in ["quit","exit"]:
            break
        else:
            cube.move(key)
