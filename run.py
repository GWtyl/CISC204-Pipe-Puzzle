
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
d = Neighbor('10', '34')
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
    p=location_propositions[random.randint(91, 100)]
    grid_setup.append(p)
    p=location_propositions[random.randint(101, 110)]
    grid_setup.append(p)
    p=location_propositions[random.randint(111, 120)]
    grid_setup.append(p)
    p=location_propositions[random.randint(121, 130)]
    grid_setup.append(p)
    p=location_propositions[random.randint(131, 140)]
    grid_setup.append(p)
    p=location_propositions[random.randint(141, 150)]
    grid_setup.append(p)
    p=location_propositions[random.randint(151, 160)]
    grid_setup.append(p)
    grid_setup.append(location_propositions[len(location_propositions)-1])
    #TODO: only same pipe and different orientation will be allowed(constraint)
    for g in grid_setup:
        if g.pipe in STRAIGHT_PIPE:
            '''constraint to make sure the pipe can be 2 opening straint pipe with different orientation at the same location'''
            E.add_constraint(Location(['N','S'], g.location)|Location(['E','W'], g.location))
        elif g.pipe in ANGLED_PIPE:
            '''constraint to make sure the pipe can be 2 opening angled pipe with different orientation at the same location'''
            E.add_constraint(Location(['N','W'], g.location)|Location(['N','E'], g.location)|Location(['S','E'], g.location)|Location(['S','W'], g.location))
        elif g.pipe in THREE_OPENING_PIPE:
            '''constraint to make sure the pipe can be 3 opening pipe with different orientation at the same location'''
            E.add_constraint(Location(['N','S','E'], g.location)|Location(['N','S','W'], g.location)|Location(['N','E','W'], g.location)|Location(['S','E','W'], g.location))
#print(f"this is the grid setup: \n{grid_setup}")
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
routes = []
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
    routes = [str(i) for i in routes]
    grid = [[1],[2,4],[1,3,5],[2,6],[1,5,7],[2,4,6,8],[5,3,9],[4,8],[7,5,9],[10,8,6],[]]


    src = 0
    dst = 10
    v = 11

    find_paths(grid,src,dst,v,int_routes)

    print(f"this is the amount of possible routes:{len(int_routes)}")
    #this is to convert all the values of int routes to string and put them in the routes list
    for i in int_routes:
        temp= []
        for j in i:
            temp.append(str(j))
        routes.append(temp)
'''change the route from ['10','11','21','31','32','33','34'] format to ['10','11'] and ['11',21],['21','31'],['31','32'],['32','33'],['33','34']'''
#TODO: constraint to make sure the path is valid; use proposition location connecvted to location CL(l1,l2)(constraint)
for i in range(len(routes)):
    for o in range(len(routes[i])-1):#this is to change the path from single one to a pair of location
        routes[i][o] = [routes[i][o],routes[i][o+1]]


'''
The goal for this week is to at least have the SAT solver working so that at least it can print something.
Ideally, we would like the solver to print in the following format:

'''

"""
IMPORTANT:
If there is a pipe in the original configuration and the correct path requires the pipe to be in a different orientation, 

"""
def example_theory():
    '''start and end piece ['E'] and ['W'] can not be connected directly'''
    E.add_constraint(~TwoPipeConnection(['E'], ['W'], '10', '11'))

    '''start and end piece ['E'] and ['W'] need to be at 10 and 34'''
    E.add_constraint(Location(['E'],'10'))
    E.add_constraint(Location(['W'],'34'))

    '''some pieces beside each other can only be connected in one way'''
    #straight(UD) pipe beside end piece can only be straight(LR) pipe
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33')&(Location(['N', 'S'],'33')))>>(Location(['E', 'W'],'33')))
    #straight(UD) pipe beside start piece can only be straight(LR) pipe
    E.add_constraint((~TwoPipeConnection(['E'], grid_setup[0].pipe, '10', '11') & (Location(['N', 'S'], '11'))) >> (Location(['E', 'W'], '11')))
    #corner 33 34 #angled pipe beside end piece can only be angled(down_left) pipe
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33') & ((Location(['N', 'W'],'33')) | (Location(['S','W'],'33'))| (Location(['S','E'],'33'))))>>(Location(['N', 'E'],'33')))
    #corner 10 11 #angled pipe beside start piece can only be angled(down_right) pipe
    E.add_constraint((~TwoPipeConnection(['E'], grid_setup[len(grid_setup)-1].pipe, '10', '11') & ((Location(['N', 'W'],'33')) | (Location(['S','W'],'33'))| (Location(['N','E'],'33'))))>>(Location(['S', 'W'],'33')))
    
    #TODO: rewrite this 3-opening can not be -| shape beside end piece or |-beside start piece 
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33')&(Location(['N', 'S','W'],'33')))>>((Location(['N', 'E', 'W'],'33'))|(Location(['N', 'S', 'E'],'33'))|(Location(['S', 'E', 'W'],'33'))))

    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '10', '11')&(Location(['N', 'S','E'],'33')))>>((Location(['N', 'E', 'W'],'33'))|(Location(['N', 'S', 'W'],'33'))|(Location(['S', 'E', 'W'],'33'))))
    
    '''nested loop go though LOCATION and check if they are in the NEIGHBORUD or NEIGHBORLR
    if they are, then they are neighbor and add them to the constraint
    if they are not, then they are not neighbor and can't be connected'''
    for loc1 in LOCATIONS:
        for loc2 in LOCATIONS:
            if [loc1, loc2] not in NEIGHBORUD and  [loc1, loc2] not in NEIGHBORLR:
                E.add_constraint(~Neighbor(loc1, loc2))
            elif [loc1, loc2] in NEIGHBORUD or [loc1, loc2] in NEIGHBORLR:
                E.add_constraint(Neighbor(loc1, loc2))
    '''check if the grid setup have a solution, if it does, the solution will be one of the routes'''
    #E.add_constraint((Is_solution(grid_setup))>>Or(*routes))
    '''change all r in route from location to location_contain_pipe'''
    #routes = [[['10','11'],['11','21'],['21','31'],['31','32'],['32','33'],['33','34']]]#test case contain 1 path
    '''route_contain = []
    for r in routes:#r is a path in routes
        possible_contain = []
        for i in range(1,len(r)-1):#loop through all location connection in path
            #print(possible_contain)
            if(i == 1 and r[i] in NEIGHBORLR):# the first grid will only habe two options, either go right(straight(LR)) or down(angled(down_left))
                possible_contain.append(contain_pt_at_Location(['E','W'],r[i][0]))#straight(LR) pipe
            elif(i == 1 and r[i] in NEIGHBORUD):
                possible_contain.append(contain_pt_at_Location(['S','W'],r[i][0]))#angled(down_left) pipe
            else:
                if r[i] in NEIGHBORLR:#current connection is from left to right
                    if(possible_contain[-1].c_pipetype == ['E','W']):#previous pipe is straight(LR) and 
                        possible_contain.append(contain_pt_at_Location(['E','W'],r[i][0]))#straight(LR) pipe
                    elif(possible_contain[-1].c_pipetype == ['N','S']):#previous pipe is straight(UD) 
                        possible_contain.append(contain_pt_at_Location(['N','E'],r[i][0]))#angled(up_right) pipe
                    elif(possible_contain[-1].c_pipetype == ['N','E']):#previous pipe is angled(top_right)
                        possible_contain.append(contain_pt_at_Location(['E','W'],r[i][0]))#straint(LR) pipe
                    elif(possible_contain[-1].c_pipetype == ['E','W']):#previous pipe is straight(LR)
                        possible_contain.append(contain_pt_at_Location(['E','W'],r[i][0]))#straint(LR) pipe
                    elif(possible_contain[-1].c_pipetype == ['S','W']):#previous pipe is angled(down_left)
                        possible_contain.append(contain_pt_at_Location(['N','E'],r[i][0]))#angled(up_right) pipe
                    elif(possible_contain[-1].c_pipetype == ['S','E']):#this cannot happen since all route goes right and down
                        possible_contain.append(contain_pt_at_Location(['N','E'],r[i][0]))
                elif(r[i] in NEIGHBORUD):#current connection is from up to down
                    if(possible_contain[-1].c_pipetype == ['S','W']):#previous pipe is angled(down_left)
                        possible_contain.append(contain_pt_at_Location(['N', 'S'],r[i][0]))#straight(UD) pipe
                    elif(possible_contain[-1].c_pipetype == ['N','S']):#previous pipe is straight(UD)
                        possible_contain.append(contain_pt_at_Location(['N','S'],r[i][0]))#straight(UD) pipe
                    elif(possible_contain[-1].c_pipetype == ['E','W']):#previous pipe is straight(LR)
                        possible_contain.append(contain_pt_at_Location(['S','W'],r[i][0]))#angled(down_left) pipe
                    elif(possible_contain[-1].c_pipetype == ['S','E']):#this cannot happen since all route goes right and down
                        possible_contain.append(contain_pt_at_Location(['N','S'],r[i][0]))
                
        route_contain.append(possible_contain)#overwrite the location to locarion_contain_pipe  '''  
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


if __name__ == "__main__":
    setup()
    # #this print[['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]
    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    '''print constraint'''
    '''for constraint in E.constraints:
        print(constraint)'''
    # After compilation (and only after), you can check some of the properties
    # of your model:
    
    print("\nSatisfiable: %s" % T.satisfiable())#True
    print("# Solutions: %d" % count_solutions(T))#number of solutions
    print("   Solution: %s" % T.solve())#solution
    
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,d,y,z], 'abcdyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))

    #E.introspect(T)
    # Check if the problem has any solution and find all solutions
    
    
    #print(f"connect: {connected_pipe}")
    
    #print(len(location_propositions))
    #print(len(pos_for_11))
    #print(possible_connectionsud)
    #print(f"grid setup: {grid_setup}")