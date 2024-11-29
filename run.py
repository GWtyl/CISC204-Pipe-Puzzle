
from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

'''These two lines make sure a faster SAT solver is used.'''
from nnf import config
config.sat_backend = "kissat"
'''import random'''
import random

'''import for BFS algorithm for finding all paths'''
from typing import List
from collections import deque
'''Encoding that will store all of your constraints'''
E = Encoding()

'''used to generate all possible orentations of a pipe'''
ORIENTATIONS = list('NSEW')

'''a visual representation of one grid's oreientation'''
'''
     N
   +----+
 W |    | E
   +----+
     S   
'''
'''this is a list of all possible locations that a pipe can be at'''
LOCATIONS = ['10', '11' , '12', '13' , '21', '22', '23', '31', '32', '33', '34']

'''this list is a list of all possible neighbours pairs that connect from up to down(N and S)'''
NEIGHBORUD = [['11','21'],['12','22'],['13','23'],['21','31'],['22','32'],['23','33']]

'''this list is a list of all possible neighbours pairs that connect from left to right(W to E)'''
NEIGHBORLR = [['10','11'],['11','12'],['12','13'],['21','22'],['22','23'],['31','32'],
            ['32','33'],['33','34']]

'''all possible type of pipe'''
TYPE = ['start','straight', 'angled', 'three_opening', 'end']

'''all possible pipe orientation at a location'''
PIPE_TYPE = []

'''A function that generates all pipe orientation'''
PIPE_TYPE = [['W'],['E']] #start and end piece will only have one orientation
for i in range(0, len(ORIENTATIONS)):#2 opeinning pipe
    orien1 = ORIENTATIONS[i]
    for j in range(i + 1, len(ORIENTATIONS)):
        orien2 = ORIENTATIONS[j]
        p=[orien1, orien2]
        PIPE_TYPE.append(p)

for i in range(0, len(ORIENTATIONS)):#3 opening pipe
    orien1 = ORIENTATIONS[i]
    for j in range(i + 1, len(ORIENTATIONS)):
        orien2 = ORIENTATIONS[j]
        for k in range(j + 1, len(ORIENTATIONS)):
            orien3 = ORIENTATIONS[k]
            p=[orien1, orien2, orien3]
            PIPE_TYPE.append(p)

'''possible pipe orientation for STRAIGHT piece'''
STRAIGHT_PIPE = [['N', 'S'], ['E', 'W']]
'''possible pipe orientation for ANGLED piece'''
ANGLED_PIPE = [['N', 'W'], ['N', 'E'], ['S', 'E'], ['S', 'W']]
'''possible pipe orientation for THREE_OPENING piece'''
THREE_OPENING_PIPE = [['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]
# #this print[['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]

'''the type of pipe(straight, angled, three_opening) can opens to these orientations'''
@proposition(E)
class Straight_Pipe(object): 
    def __init__(self, type, pipe_specific) -> None:
        assert type in TYPE
        assert pipe_specific in STRAIGHT_PIPE
        self.type = type
        self.pipe_specific = pipe_specific
    def _prop_name(self):
        return f"({self.type} opens {self.pipe_specific})"
@proposition(E)
class Angled_Pipe(object): 
    def __init__(self, type, pipe_specific) -> None:
        assert type in TYPE
        assert pipe_specific in ANGLED_PIPE
        self.type = type
        self.pipe_specific = pipe_specific
    def _prop_name(self):
        return f"({self.type} opens {self.pipe_specific})"

@proposition(E)
class Three_Opening_Pipe(object): 
    def __init__(self, type, pipe_specific) -> None:
        assert type in TYPE
        assert pipe_specific in THREE_OPENING_PIPE
        self.type = type
        self.pipe_specific = pipe_specific
    def _prop_name(self):
        return f"({self.type} opens {self.pipe_specific})"


'''given pipe is at given location; this works for the setup'''
@proposition(E)
class Location(object): 
    def __init__(self, pipe, location) -> None:
        assert pipe in PIPE_TYPE
        assert location in LOCATIONS
        self.pipe = pipe
        self.location = location
    def _prop_name(self):
        return f"({self.pipe} @ {self.location})"
    
'''two pipe at given location is connected'''
@proposition(E)
class TwoPipeConnection(object):
    def __init__(self, pipe1, pipe2, location1, location2) -> None:
        assert pipe1 in PIPE_TYPE
        assert pipe2 in PIPE_TYPE
        assert location1 in LOCATIONS
        assert location2 in LOCATIONS
        #check if this is a valid connection
        #assert [location1,location2] in NEIGHBORUD or [location1,location2] in NEIGHBORLR, f"Invalid connection: {location1} and {location2}"
        self.pipe1 = pipe1
        self.pipe2 = pipe2
        self.location1 = location1
        self.location2 = location2

    def _prop_name(self):
        return f"({self.pipe1}@{self.location1} is connected to {self.pipe2}@{self.location2})"

'''this is a pipetype
TODO: may need to separate this into 5 different classes()'''
@proposition(E)
class PipeType(object):
    def __init__(self, pipe) -> None:
        assert pipe in PIPE_TYPE
        self.pipe = pipe

    def _prop_name(self):
        return f"PipeType({self.pipe})"
    
'''TODO: what does this do?'''
#J: does this check for whether or not the pipes are connected?
@proposition(E)
class Connected(object):
    def __init__(self, pipe1, pipe2) -> None:
        assert pipe1 in PIPE_TYPE
        assert pipe2 in PIPE_TYPE
        self.pipe1 = pipe1
        self.pipe2 = pipe2

    def _prop_name(self):
        return f"Connected({self.pipe1}, {self.pipe2})"

'''given pipe is a given pipe type (like straight, angled, three_opening)'''
@proposition(E)
class Pipe_type_orien_at_Location(object):
    def __init__(self, pipe, type):
        assert pipe in PIPE_TYPE
        assert type in TYPE
        self.type = type
        self.pipe = pipe
    def _prop_name(self):
        return f"[{self.type} is a {self.pipe}]"

'''each grid can only be traversed once'''
@proposition(E)
class traverse_once(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        self.loc = loc
    def _prop_name(self):
        return f"[{self.loc} has been traversed]"

'''given two locations are neighbors (they are beside each other)'''
@proposition(E)
class Neighbor(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        #assert [loc1,loc2] in NEIGHBORUD or [loc1,loc2] in NEIGHBORLR, f"Invalid connection: {loc1} and {loc2}"
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[Neighbor({self.loc1}, {self.loc2})]"
    
'''given location contain a given pipe type'''
@proposition(E)
class contain_pt_at_Location(object):
    def __init__(self, c_pipetype, l) -> None:
        assert l in LOCATIONS
        assert c_pipetype in PIPE_TYPE
        self.l = l
        self.c_pipetype = c_pipetype

    def _prop_name(self):
        return f"[{self.l} contain{self.c_pipetype}]"

'''solution for the grid'''
@proposition(E)
class Is_solution(object):
    def __init__(self, setup) -> None:
        self.setup = setup

    def _prop_name(self):
        return f"[{self.setup} have solution]"

'''prevent the code below from bugging'''
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:
    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = Location(['E'],'10')# there must have a start piece at 10
b = Location(['W'],'34')# there must have a end piece at 34
c = TwoPipeConnection(['E'], ['W'], '10', '11')#start and end piece ['E'] and ['W'] will not be connected directly
d = Neighbor('11', '21')#11 and 21 are neighbors
e = FancyPropositions("e")

# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")

'''this generates all possible location with all possible pipe orientation; all possible setup for the grid'''
location_propositions = []
for l in LOCATIONS:
    if(l == '10'):
        location_propositions.append(Location(PIPE_TYPE[1], l))
    elif(l == '34'):
        location_propositions.append(Location(PIPE_TYPE[0], l))
    else:
        for i in range(2,len(PIPE_TYPE)):
            p=PIPE_TYPE[random.randint(2, len(PIPE_TYPE)-1)]
            location_propositions.append(Location(p, l))
grid_setup  = []
def setup():
    '''select one setup from location_propositions; also made sure we have exactly one pipe on each location'''
    grid_setup.append(location_propositions[0])
    grid_setup.append(location_propositions[random.randint(1, 10)])
    #this for loop does the same thing as the rest of the code it's easier to read
    #can decide if you want to use the for loop or hard code
    for i in range(11,82,10):
        p = location_propositions[random.randint(i,i+9)]
        grid_setup.append(p)
    '''
    p=location_propositions[random.randint(11, 20)]
    grid_setup.append(p)
    p=location_propositions[random.randint(21, 30)]
    grid_setup.append(p)
    p=location_propositions[random.randint(31, 40)]
    grid_setup.append(p)
    p=location_propositions[random.randint(41, 50)]
    grid_setup.append(p)
    p=location_propositions[random.randint(51, 60)]
    grid_setup.append(p) 
    p=location_propositions[random.randint(61, 70)]
    grid_setup.append(p)
    p=location_propositions[random.randint(71, 80)]
    grid_setup.append(p)
    p=location_propositions[random.randint(81, 90)]
    grid_setup.append(p)'''
    grid_setup.append(location_propositions[len(location_propositions)-1])
grid_setup = [
    Location(['E'], '10'),
    Location(['N', 'W'], '11'),
    Location(['S', 'E'], '12'),
    Location(['N', 'E'], '13'),
    Location(['E', 'W'], '21'),
    Location(['S', 'E'], '22'),
    Location(['N', 'E', 'W'], '23'),
    Location(['N', 'S', 'E'], '31'),
    Location(['N', 'S', 'E'], '32'),
    Location(['N', 'S', 'E'], '33'),
    Location(['W'], '34')
]
#just pick one setup from for now
def location_to_index(l):
    if l == '10':
        return 0
    elif l == '11':
        return 1
    elif l == '12':
        return 2
    elif l == '13':
        return 3
    elif l == '21':
        return 4
    elif l == '22':
        return 5
    elif l == '23':
        return 6
    elif l == '31':
        return 7
    elif l == '32':
        return 8
    elif l == '33':
        return 9
    elif l == '34':
        return 10
    else:
        return -1
#-> means the function should return nothing
# path: List[int] means the path variable should be a list of integers
#this function is to print the traversable path from starting pipe to ending pipe
def print_path(path: List[int]) -> None:
    for i in range(len(path)):
        print(path[i], end = " ")
    print()

#check if a node/position is visited or not    
def is_not_visited(x : int, path: List[int]) -> int:
    for i in range(len(path)):
        if (path[i] == x):
            return 0
    return 1

#this is to convert the values from 0,1,2,3...10 to location notation (10,11,12,...34)
#since the finding all the possible route function breaks if it's not listed ast 0,1,2,3,4...
#this function is necessary to convert it to proper notation
def convert_value(val):
    new_val = []
    for i in val:
        match i:
            case 0: 
                new_val.append(10)
            case 1:
                new_val.append(11)
            case 2:
                new_val.append(12)
            case 3:
                new_val.append(13)
            case 4:
                new_val.append(21)
            case 5:
                new_val.append(22)
            case 6:
                new_val.append(23)
            case 7:
                new_val.append(31)
            case 8:
                new_val.append(32)
            case 9:
                new_val.append(33)
            case 10:
                new_val.append(34)
            case _:
                new_val.append("does not exist")
    return new_val
'''
find all possible paths for a graph/grid
g: the grid/graph
src: the starting point
dst: the ending point
v: number of verticies
'''    

def find_paths(g: List[List[int]], src: int, dst: int, v: int, routes: List[int]) -> None:
    #queue to store the paths
    q = deque()
    
    #path vector to store the current vectors
    path = []
    path.append(src)
    q.append(path.copy())
    
    while q:
        path = q.popleft()
        last = path[len(path) - 1]
        
        if(last == dst):
            new_val = convert_value(path)
            #print_path(path)
            routes.append(new_val)
            
        for i in range(len(g[last])):
            if(is_not_visited(g[last][i],path)):
                new_path = path.copy()
                new_path.append(g[last][i])
                q.append(new_path)
    
        
#all possible routes for the grid
int_routes = []
routes = []
routes = [str(i) for i in routes]
grid = [[1],[2,4],[1,3,5],[2,6],[1,5,7],[2,4,6,8],[5,3,9],[4,8],[7,5,9],[10,8,6],[]]
#create a new grid that has one sided connection only
new_grid = [[1],[2,4],[3,5],[6],[7,5],[8,6],[9],[8],[9],[10],[]]
src = 0
dst = 10
v = 11
find_paths(new_grid,src,dst,v,int_routes)

#(f"this is the amount of possible routes:{len(int_routes)}")
#this is to convert all the values of int routes to string and put them in the routes list
for i in int_routes:
    temp= []
    for j in i:
        temp.append(str(j))
    routes.append(temp)
'''change the route from ['10','11','21','31','32','33','34'] format to ['10','11'] and ['11',21],['21','31'],['31','32'],['32','33'],['33','34']'''

#TODO: constraint to make sure the path is valid; use proposition location connected to location CL(l1,l2)(constraint)
for i in range(len(routes)):
    for o in range(len(routes[i])-1):#this is to change the path from single one to a pair of location
        routes[i][o] = [routes[i][o],routes[i][o+1]]
        #E.add_constraint(Connected())


'''
The goal for this week is to at least have the SAT solver working so that at least it can print something.
Ideally, we would like the solver to print in the following format:

'''

"""
IMPORTANT:
If there is a pipe in the original configuration and the correct path requires the pipe to be in a different orientation, 

"""
def example_theory():
    #TODO: only same pipe and different orientation will be allowed(constraint)
    for g in grid_setup:
        if g.location == '10':#start piece can only have ['E'] orientation
            E.add_constraint(Location(['E'], g.location))
        elif g.location == '34':#end piece can only have ['W'] orientation
            E.add_constraint(Location(['W'], g.location))
        elif g.pipe in THREE_OPENING_PIPE:
            '''constraint to make sure the pipe can be 3 opening pipe with different orientation at the same location'''
            #3-opening can not be -| shape beside end piece or |-beside start piece 
            if g.location == '11':
                E.add_constraint((~Location(['N','S','E'], g.location))&(~TwoPipeConnection(['E'], ['N','S','E'], '10', g.location)))
            elif g.location == '33':
                E.add_constraint((~Location(['N', 'S', 'W'], g.location))&(~TwoPipeConnection(['N', 'S', 'W'], ['W'], g.location, '11')))
            else:
                constraint.add_exactly_one(E, [Location(['N','S','E'], g.location), Location(['N','S','W'], g.location), Location(['N','E','W'], g.location), Location(['S','E','W'], g.location)])
        elif g.pipe in ANGLED_PIPE:
            #UP_RIGHT and UP_LEFT will be location 32
            #DOWN_RIGHT and DOWN_LEFT will be location 12
            #UP_RIGHT and DOWN_RIGHT will be location 21
            #UP_LEFT and DOWN_LEFT will be location 23 #partial true, need limit
            #TODO:connection check for each location 
            if g.location == '11':
                E.add_constraint((Location(['S','W'], g.location))&(TwoPipeConnection(['E'], ['S','W'], '10', g.location)))
            elif g.location == '33':
                E.add_constraint((Location(['N','E'], g.location))&(TwoPipeConnection(['N','E'], ['W'], g.location, '34')))           
        elif g.pipe in STRAIGHT_PIPE:#maybe constraint this last so it can use the constraint above
            #this make sure only straight pipe(LR) can be beside start and end piece and they are not connected
            if g.location == '11':
                E.add_constraint((Location(['E','W'], g.location))&TwoPipeConnection(['E'], ['E','W'], '10', g.location))
            elif g.location == '13':#if it is at 13, it can not connect to 12 or 23
                E.add_constraint((Location(g.pipe, g.location))&(~TwoPipeConnection(grid_setup[2].pipe, g.pipe, grid_setup[2].location, g.location)&(~TwoPipeConnection(g.pipe, grid_setup[6].pipe, g.location, grid_setup[6].location))))
            elif g.location == '31':#if it is at 31, it stay same oreietation but no connction to the pipe at location 32 or 21
                E.add_constraint((Location(g.pipe, g.location))&(~TwoPipeConnection(g.pipe, grid_setup[8].pipe, g.location, grid_setup[8].location)&(~TwoPipeConnection(g.pipe, grid_setup[4].pipe, g.location, grid_setup[4].location))))
            elif g.location == '33':
                E.add_constraint((Location(['E','W'], g.location))&TwoPipeConnection(['E','W'], ['W'], g.location, '34'))
            elif  g.location == '22':#any other location(22) have 2 possible orientation: straight pipe(LR) or straight pipe(UD)
                '''constraint to make sure the pipe can be 2 opening straint pipe with different orientation at the same location'''
                constraint.add_exactly_one(E, [Location(['E','W'], g.location), Location(['N','S'], g.location)])
        
    '''start and end piece ['E'] and ['W'] can not be connected directly'''
    E.add_constraint(~TwoPipeConnection(['E'], ['W'], '10', '34'))
    
    '''nested loop go though LOCATION and check if they are in the NEIGHBORUD or NEIGHBORLR
    if they are, then they are neighbor and add them to the constraint
    if they are not, then they are not neighbor and can't be connected'''
    for loc1 in LOCATIONS:
        for loc2 in LOCATIONS:
            if [loc1, loc2] in NEIGHBORUD or [loc1, loc2] in NEIGHBORLR:
                E.add_constraint(Neighbor(loc1, loc2))
            else:
                E.add_constraint(~Neighbor(loc1, loc2))
            """if [loc1, loc2] not in NEIGHBORUD and  [loc1, loc2] not in NEIGHBORLR:
                E.add_constraint(~Neighbor(loc1, loc2))
            elif [loc1, loc2] in NEIGHBORUD or [loc1, loc2] in NEIGHBORLR:
                E.add_constraint(Neighbor(loc1, loc2))"""
    
    #this is to check whether or not two pipes are connected
    #note that one pipe can be connected to multiple pipes
    tempconnect = []
    #print(f"this is grid setup: \n {grid_setup}")
    for i in range(1,len(grid_setup)-1):
        pos1 = grid_setup[i]
        pos2 = grid_setup[i+1]       
        if(i == 3 or i== 6):
            continue
        elif ('E' in pos1.pipe and 'W' in pos2.pipe):
            tempconnect.append([pos1,pos2])
            E.add_constraint(Neighbor(pos1.location,pos2.location))
            #print(f"pipe at {grid_setup[i].location} can connect to pipe at {grid_setup[j].location}")
            #E.add_constraint((Neighbor(grid_setup[i].location,grid_setup[j].location)|Neighbor(grid_setup[j].location,grid_setup[i].location))>>(TwoPipeConnection(grid_setup[i].pipe,grid_setup[j].pipe,grid_setup[i].location,grid_setup[j].location)))
    for i in range(1,7):
        pos1 = grid_setup[i]
        pos2 = grid_setup[i+3]
        if('S' in pos1.pipe and 'N' in pos2.pipe):
            tempconnect.append([pos1,pos2])
            E.add_constraint(Neighbor(pos1.location,pos2.location))
            
    '''find a list which contain 'E','W' and a list contain 'N','S' and a list contain 'N','E' and a list contain 'S','W' total of 4 list'''
    list_EW = []
    list_NS = []
    list_NE = []
    list_SW = []

    for p in PIPE_TYPE:
        if 'E' in p and 'W' in p:
            list_EW.append(p)
        if 'N' in p and 'S' in p:
            list_NS.append(p)
        if 'N' in p and 'E' in p:
            list_NE.append(p)
        if 'S' in p and 'W' in p:
            list_SW.append(p)
    '''TODO:use every route in routes to create a constraint that will make sure only these route is valid'''
    '''change the route from ['10','11','21','31','32','33','34'] format to ['10','11'] and ['11',21],['21','31'],['31','32'],['32','33'],['33','34']'''
    '''#TODO: constraint to make sure the path is valid; use proposition location connecvted to location CL(l1,l2)(constraint)
    for i in range(len(routes)):
        for o in range(len(routes[i])-1):#this is to change the path from single one to a pair of location
            routes[i][o] = [routes[i][o],routes[i][o+1]]'''
    for r in routes[:6]:  # take the first 6 solution routes
        for i in range(1, len(r) - 1):  # take one connection out of the route and skip the first and last location
            if r[i] in NEIGHBORLR:  # current connection is from left to right and next connection is from left to right
                if r[i - 1] in NEIGHBORLR:
                    list_EW_as_constraint = []
                    for p in list_EW:
                        list_EW_as_constraint.append(Location(p, r[i][0]))
                    if r[i][0] == '12' or r[i][0] == '32':
                        E.add_constraint(Location(['E','W'], r[i][0]))
            elif r[i] in NEIGHBORUD:  # current connection is from up to down and next connection is from up to down
                if r[i - 1] in NEIGHBORUD:
                    list_NS_as_constraint = []
                    for p in list_NS:
                        list_NS_as_constraint.append(Location(p, r[i][0]))
                    #(LR) for location 12 and 32 
                    #(UD) for location 21 and 23 #if it is in the solution routes
                    if r[i][0] == '21' or r[i][0] == '23':
                        E.add_constraint(Location(['N','S'], r[i][0]))
                        #TODO: add constraint for connection
            elif r[i] in NEIGHBORUD:  # current connection is from up to down and next connection is from left to right
                if r[i - 1] in NEIGHBORLR:
                    list_NE_as_constraint = []
                    for p in list_NE:
                        list_NE_as_constraint.append(Location(p, r[i][0]))
                    E.add_constraint(Location(['N','E'], r[i][0]))
                    #TODO: add other angled pipe constraint
            elif r[i] in NEIGHBORLR:  # current connection is from left to right and next connection is from up to down
                if r[i - 1] in NEIGHBORUD:
                    list_SW_as_constraint = []
                    for p in list_SW:
                        list_SW_as_constraint.append(Location(p, r[i][0]))
                    if r[i][0] == '12':
                        E.add_constraint(Location(['S','W'], r[i][0]))
                    
                
    
    #TODO: decide wheather this code will help the goal we currently have        
    '''check if how many pairs on grid is connected.if they are connected, add them to constriant
    loop through NeighborUD and NeighborLR
    this is basically checking to see if there is a pair of pipe that is connected
    these only check for pairs, meaning only checking if two pipes are connected, not if 3 pipes or 4 pipes etc are connected'''
    '''connected_pipe = []
    pair_pipe = []
    for i in range(0,len(grid_setup)):
        for connectLR in NEIGHBORLR:
            if connectLR[0] == grid_setup[i].location and connectLR[1] == grid_setup[i+1].location:
                if "E" in grid_setup[i].pipe and "W" in grid_setup[i+1].pipe:
                    pair_pipe.append(grid_setup[i])
                    pair_pipe.append(grid_setup[i+1])
                    connected_pipe.append(pair_pipe)
                    pair_pipe = []
                    break'''

    #TODO: decide wheather this code will help the goal we currently have; we now check connection based on the routes
    '''this is to check if there are pairs of pipes connected north/south
    it does the same thing as the loop above except this checks if a pair of pipes are connected north/south
    so if a pipe has a opening upwards and a pipe has a opening downwards then they are connected'''
    '''for i in range(0,2):
        for j in range(1,4):            
            for connectUD in NEIGHBORUD:
                if connectUD[0] == grid_setup[j+ 3*i].location and connectUD[1] == grid_setup[j+3*(i+1)].location:
                    if "S" in grid_setup[j+ 3*i].pipe and "N" in grid_setup[j+3*(i+1)].pipe:
                        pair_pipe.append(grid_setup[j+ 3*i])
                        pair_pipe.append(grid_setup[j+3*(i+1)])
                        connected_pipe.append(pair_pipe)
                        pair_pipe = []
                        break'''
    
    #TODO: Connected(p1,p2) if p1 and p2 are connected(constraint)
    '''all possible connection like [E,[E,W]] start pipe at 10 can connect to straight pipe'''
    possible_connectionsud = []
    for i in PIPE_TYPE:
        for j in i:
            if j == "S":
                for x in PIPE_TYPE:
                    for y in x:
                        if y == "N":
                            c=[i,x]
                            possible_connectionsud.append(c)    
            else:
                break  
    #constraint.add_exactly_one(E, possible_connectionsud)
    possible_connectionslr = []
    for i in PIPE_TYPE:
        for j in i:
            if j == "E":
                for k in PIPE_TYPE:
                    for a in k:
                        if a == "W":
                            c=[i,k]
                            possible_connectionslr.append(c)
    possible_connectionslr.remove([['E'], ['W']])
    #constraint.add_exactly_one(E, possible_connectionslr)
    
    
    '''for one location, there are at least one and at most 4 neighbor'''
    '''TODO: rewrite this so it is working, also 10 cannot connect to 34, 11 cannot connect to 33, 12 cannot connect to 32, 13 cannot connect to 31
        like this E.add_constraint(~TwoPipeConnection(['E'], ['W'], '10', '11')) make sure one pipe at a location can only connect to its neighbor'''
    '''all_possible_neighbor = []
    for l in LOCATIONS:
        possible_neighbor = []
        for nud in NEIGHBORUD:
            if l in nud:
                possible_neighbor.append(Neighbor(nud[0],nud[1]))
        for nud in NEIGHBORLR:
            if l in nud:
                possible_neighbor.append(Neighbor(nud[0],nud[1]))
        all_possible_neighbor.append(possible_neighbor)
    constraint.add_exactly_one(E, all_possible_neighbor)
    print(all_possible_neighbor)'''
    

    
    return E

def display_solution(S, want=False):
    true_props = set()
    for k in S:
        if S[k] and (not want or '@' in str(k)):
            true_props.add(str(k)+' is '+str(S[k]))
    print("\n".join(true_props))
if __name__ == "__main__":
    #setup()
    #print(f"this is the grid setup: \n{grid_setup}")
    for r in routes[:6]:    
        print(r)
    # #this print[['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]
    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    S = T.solve()
    if S:
        display_solution(S, True)
    else:
        print("No solution!!")
    # After compilation (and only after), you can check some of the properties
    # of your model:
    
    '''print("\nSatisfiable: %s" % T.satisfiable())#True
    print("# Solutions: %d" % count_solutions(T))#number of solutions
    print("   Solution: %s" % T.solve())#solution'''
    
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,d,y,z], 'abcdyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))

    #E.introspect(T)
