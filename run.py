
from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood
'''test for git M'''

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
#import random
import random

#import for BFS algorithm for finding all paths
from typing import List
from collections import deque
# Encoding that will store all of your constraints
E = Encoding()

ORIENTATIONS = list('NSEW')
#     N
#   +----+
# W |    | E
#   +----+
#     S   
LOCATIONS = ['10', '11' , '12', '13' , '21', '22', '23', '31', '32', '33', '34']

#win condition: go through neighbor array and make sure every pair of neighbor is connected
NEIGHBORUD = [['11','21'],['12','22'],['13','23'],['21','31'],['22','32'],['23','33']]

NEIGHBORLR = [['10','11'],['11','12'],['12','13'],['21','22'],['22','23'],['31','32'],
            ['32','33'],['33','34']]
#all possible type of pipe
TYPE = ['straight', 'angled', 'three_opening']

PIPE_TYPE = [['W'],['E']]
for i in range(0, len(ORIENTATIONS)):
    orien1 = ORIENTATIONS[i]
    for j in range(i + 1, len(ORIENTATIONS)):
        orien2 = ORIENTATIONS[j]
        p=[orien1, orien2]
        PIPE_TYPE.append(p)

for i in range(0, len(ORIENTATIONS)):
    orien1 = ORIENTATIONS[i]
    for j in range(i + 1, len(ORIENTATIONS)):
        orien2 = ORIENTATIONS[j]
        for k in range(j + 1, len(ORIENTATIONS)):
            orien3 = ORIENTATIONS[k]
            p=[orien1, orien2, orien3]
            PIPE_TYPE.append(p)
#print(pipe_type)



#a pipe at this location
@proposition(E)
class Location(object): 
    def __init__(self, pipe, location) -> None:
        assert pipe in PIPE_TYPE
        assert location in LOCATIONS
        self.pipe = pipe
        self.location = location
    def _prop_name(self):
        return f"({self.pipe} @ {self.location})"
    
#two pipe  at these location is connected
@proposition(E)
class TwoPipeConnection(object):
    def __init__(self, pipe1, pipe2, location1,location2) -> None:
        assert pipe1 in PIPE_TYPE
        assert pipe2 in PIPE_TYPE
        assert location1 in LOCATIONS
        assert location2 in LOCATIONS
        self.pipe1 = pipe1
        self.pipe2 = pipe2
        self.location1 = location1
        self.location2 = location2

    def _prop_name(self):
        return f"({self.pipe1}@{self.location1} -> {self.pipe2}@{self.location1})"
@proposition(E)
class PipeType(object):
    def __init__(self, pipe) -> None:
        assert pipe in PIPE_TYPE
        self.pipe = pipe

    def _prop_name(self):
        return f"PipeType({self.pipe})"
@proposition(E)
class Connected(object):
    def __init__(self, pipe1, pipe2) -> None:
        assert pipe1 in PIPE_TYPE
        assert pipe2 in PIPE_TYPE
        self.pipe1 = pipe1
        self.pipe2 = pipe2

    def _prop_name(self):
        return f"Connected({self.pipe1}, {self.pipe2})"
@proposition(E)
class Pipe_type_orien_at_Location(object):
    def __init__(self, pipe, type):
        assert pipe in PIPE_TYPE
        assert type in TYPE
        self.type = type
        self.pipe = pipe
    def _prop_name(self):
        return f"[{self.type} is a {self.pipe}]"
@proposition(E)
class Neighbor(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[{self.loc1} --> {self.loc2}]"
@proposition(E)
class contain_pt_at_Location(object):
    def __init__(self, c_pipetype, l) -> None:
        assert l in LOCATIONS
        assert c_pipetype in PIPE_TYPE
        self.l = l
        self.c_pipetype = c_pipetype

    def _prop_name(self):
        return f"[{self.l} contain{self.c_pipetype}]"


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
c = FancyPropositions("c")
d = FancyPropositions("d")
e = FancyPropositions("e")

# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")

#all possible setup for the whole grid
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
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
#  Change the name to something else. This is still using the example name
def example_theory():
    
    
    #select one config; also made sure we have exactly one pipe on each location
    grid_setup  = []
    grid_setup.append(location_propositions[0])
    grid_setup.append(location_propositions[random.randint(1, 10)])
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
    grid_setup.append(p)
    grid_setup.append(location_propositions[len(location_propositions)-1])
    E.add_constraint(And(*grid_setup))#imply the there are different orientation for the setup with all same pipe
    


    #-> means the function should return nothing
    # path: List[int] means the path variable should be a list of integers
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
                print_path(path)
                routes.append(path)
                
            #print(len(g[last]))
            for i in range(len(g[last])):
                if(is_not_visited(g[last][i],path)):
                    new_path = path.copy()
                    new_path.append(g[last][i])
                    q.append(new_path)
    
        
    #all possible routes for the grid
    routes = []
    grid = [[1],[2,4],[1,3,5],[2,6],[1,5,7],[2,4,6,8],[5,3,9],[4,8],[7,5,9],[10,8,6],[]]
    src = 0
    dst = 10
    v = 11
    find_paths(grid,src,dst,v,routes)
    
    '''possible orientations for each pipe'''
    straight_pipes = []
    angled_pipes = []
    three_opening_pipes = []

    for pipe in PIPE_TYPE:
        if len(pipe) == 2:
            if pipe == ['N', 'S'] or pipe == ['E', 'W']:
                straight_pipes.append(Pipe_type_orien_at_Location(pipe,'straight'))
            else:
                angled_pipes.append(pipe)
        elif len(pipe) == 3:
            three_opening_pipes.append(pipe)
    #find all what a pipe need to contain at one location
    routes = [[['10','11'],['11','12'],['12','13'],['13','23'],['23','33'],['33','34']]]#test case for possible_cotain
    possible_contain = []
    for r in routes:
        for i in range(1,len(r)):
            if(i == 1 and r[i] in NEIGHBORLR):
                possible_contain.append(contain_pt_at_Location(['E','W'],r[i][0]))
            elif(i == 1 and r[i] in NEIGHBORUD):
                possible_contain.append(contain_pt_at_Location(['S','W'],r[i][0]))
            else:
                print(r[i] in NEIGHBORLR , possible_contain[i-2].c_pipetype,i)
                if r[i] in NEIGHBORLR:
                    if(possible_contain[i-2].c_pipetype == ['E','W']):
                        possible_contain.append(contain_pt_at_Location(['E','W'],r[i][0]))
                    elif(possible_contain[i-2].c_pipetype == ['N','S']):
                        possible_contain.append(contain_pt_at_Location(['N','E'],r[i][0]))
                elif(r[i] in NEIGHBORUD and possible_contain[i-2].c_pipetype == ['S','W']):
                    possible_contain.append(contain_pt_at_Location(['N', 'S'],r[i][0]))
                elif(r[i] in NEIGHBORUD and possible_contain[i-2].c_pipetype == ['E','W']):
                    possible_contain.append(contain_pt_at_Location(['S','W'],r[i][0]))
    #[['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]          
    print(possible_contain)#[[11 contain['E', 'W']], [12 contain['E', 'W']], [13 contain['S', 'W']], [23 contain['N', 'S']]]
            




    connected_pipe = []
    pair_pipe = []
    #check if how many pairs on grid is connected.if they are connected, add them to constriant
    #loop through UD and LR
    for i in range(0,len(grid_setup)):
        for connectLR in NEIGHBORLR:
            if connectLR[0] == grid_setup[i].location and connectLR[1] == grid_setup[i+1].location:
                if "E" in grid_setup[i].pipe and "W" in grid_setup[i+1].pipe:
                    pair_pipe.append(grid_setup[i])
                    pair_pipe.append(grid_setup[i+1])
                    connected_pipe.append(pair_pipe)
                    pair_pipe = []
                    break
    for i in range(0,2):
        for j in range(1,4):            
            for connectUD in NEIGHBORUD:
                if connectUD[0] == grid_setup[j+ 3*i].location and connectUD[1] == grid_setup[j+3*(i+1)].location:
                    if "S" in grid_setup[j+ 3*i].pipe and "N" in grid_setup[j+3*(i+1)].pipe:
                        pair_pipe.append(grid_setup[j+ 3*i])
                        pair_pipe.append(grid_setup[j+3*(i+1)])
                        connected_pipe.append(pair_pipe)
                        pair_pipe = []
                        break

    E.add_constraint(And(*connected_pipe))
    
    #all possible connection [E,[E,W]]
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
    constraint.add_exactly_one(E, possible_connectionsud)
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
    constraint.add_exactly_one(E, possible_connectionslr)

    #for one location, there are at least one and at most 4 neighbor
    all_possible_neighbor = []
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
    #TODO: add constriant for grid_setup
    #TODO: give out a solution based on the grid_setup and connected_pipe
    #start and end piece ['E'] and ['W'] will not be connected directly
    E.add_constraint(~TwoPipeConnection(['E'], ['W'], '10', '11'))
    #start and end piece ['E'] and ['W'] need to be at 10 and 34
    E.add_constraint(Location(['E'],'10'))
    E.add_constraint(Location(['W'],'34'))
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33')&(Location(['N', 'S'],'33')))>>(Location(['E', 'W'],'33')))
    E.add_constraint((~TwoPipeConnection(['E'], grid_setup[0].pipe, '10', '11') & (Location(['N', 'S'], '11'))) >> (Location(['E', 'W'], '11')))
    #corner 33 34
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33') & ((Location(['N', 'W'],'33')) | (Location(['S','W'],'33'))| (Location(['S','E'],'33'))))>>(Location(['N', 'E'],'33')))
    #corner 10 11
    E.add_constraint((~TwoPipeConnection(['E'], grid_setup[len(grid_setup)-1].pipe, '10', '11') & ((Location(['N', 'W'],'33')) | (Location(['S','W'],'33'))| (Location(['N','E'],'33'))))>>(Location(['S', 'W'],'33')))

    # T shape 33 34
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33')&(Location(['N', 'S','W'],'33')))>>((Location(['N', 'E', 'W'],'33'))|(Location(['N', 'S', 'E'],'33'))|(Location(['S', 'E', 'W'],'33'))))

    # T shape 10 11
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '10', '11')&(Location(['N', 'S','E'],'33')))>>((Location(['N', 'E', 'W'],'33'))|(Location(['N', 'S', 'W'],'33'))|(Location(['S', 'E', 'W'],'33'))))
    
    return E


if __name__ == "__main__":
    #print(PIPE_TYPE)
    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    '''print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))'''
    
    #E.introspect(T)
    # Check if the problem has any solution and find all solutions
    
    
    #print(f"connect: {connected_pipe}")
    
    #print(len(location_propositions))
    #print(len(pos_for_11))
    #print(possible_connectionsud)
    #print(f"grid setup: {grid_setup}")