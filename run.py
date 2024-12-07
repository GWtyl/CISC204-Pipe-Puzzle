from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
import random
from pprint import pprint
# Encoding that will store all of your constraints
E = Encoding()
'''all the locations in the grid'''
LOCATIONS = [10, 11, 12, 13, 21, 22, 23, 31, 32, 33, 34]
'''list of neighbors'''
NB = []

'''used to generate all possible orentations of a pipe'''
ORIENTATIONS = list('NSEW')

'''a visual representation of one grid cell

     N
   +----+
 W |    | E
   +----+
     S   
'''

'''used to generate all possible orentations of a pipe'''
#the following loop give: [['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]
PIPE_ORIENTATIONS = [['W'],['E']]
for i in range(0, len(ORIENTATIONS)):#2 opeinning pipe
    orien1 = ORIENTATIONS[i]
    for j in range(i + 1, len(ORIENTATIONS)):
        orien2 = ORIENTATIONS[j]
        p=[orien1, orien2]
        PIPE_ORIENTATIONS.append(p)
for i in range(0, len(ORIENTATIONS)):#3 opening pipe
    orien1 = ORIENTATIONS[i]
    for j in range(i + 1, len(ORIENTATIONS)):
        orien2 = ORIENTATIONS[j]
        for k in range(j + 1, len(ORIENTATIONS)):
            orien3 = ORIENTATIONS[k]
            p=[orien1, orien2, orien3]
            PIPE_ORIENTATIONS.append(p)

'''possible pipe orientation for STRAIGHT pipe'''
STRAIGHT_PIPE = []#this will contain:[['N', 'S'], ['E', 'W']] after the loop
'''possible pipe orientation for ANGLED pipe'''
ANGLED_PIPE = []#this will contain:[['N', 'W'], ['N', 'E'], ['S', 'E'], ['S', 'W']] after the loop
'''possible pipe orientation for THREE_OPENING pipe'''
THREE_OPENING_PIPE = []#this will contain:[['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']] after the loop
'''initialize orientations for each type of pipe'''
for p in PIPE_ORIENTATIONS:
    if len(p) == 2:
        if ('N' in p and 'S' in p) or ('E' in p and 'W' in p):
            STRAIGHT_PIPE.append(p)
        else:
            ANGLED_PIPE.append(p)
    elif len(p) == 3:
        THREE_OPENING_PIPE.append(p)

'''given pipe is at given location'''
@proposition(E)
class Location(object): 
    def __init__(self, pipe, location) -> None:
        assert pipe in PIPE_ORIENTATIONS
        assert location in LOCATIONS
        self.pipe = pipe
        self.location = location
    def _prop_name(self):
        return f"({self.pipe} @ {self.location})"

'''the pipes at these two locations are connected'''
@proposition(E)
class Connected(object):
    def __init__(self, l1, l2) -> None:
        assert l1 in LOCATIONS
        assert l2 in LOCATIONS
        self.l1 = l1
        self.l2 = l2

    def _prop_name(self):
        return f"Connected({self.l1}, {self.l2})"

'''pipe at this location have opeing facing east'''
@proposition(E)
class Have_to_east(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        self.loc = loc

    def _prop_name(self):
        return f"{self.loc} can go East"
'''pipe at this location have opeing facing south'''
@proposition(E)
class Have_to_south(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        self.loc = loc

    def _prop_name(self):
        return f"{self.loc} can go South"
'''pipe at this location have opeing from west''' 
@proposition(E)
class Have_from_west(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        self.loc = loc

    def _prop_name(self):
        return f"{self.loc} can come from West"
'''pipe at this location have opeing from north'''
@proposition(E)
class Have_from_north(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        self.loc = loc

    def _prop_name(self):
        return f"{self.loc} can come from North"

'''grid has a solution from location 10 to 34'''
class Solution(object):
    def __init__(self,loc1,loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2
    def _prop_name(self):
        return f"Solution from {self.loc1} to {self.loc2})"
    
'''two locations are neighbors (they are beside each other)'''
@proposition(E)
class NeighborLR(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[NeighborLR({self.loc1}, {self.loc2})]"

'''two locations are neighbors (they are on top of each other)'''
@proposition(E)
class NeighborUD(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[NeighborUD({self.loc1}, {self.loc2})]"
    
'''the location has no pipe on it'''
@proposition(E)
class Empty(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        self.loc = loc

    def _prop_name(self):
        return f"Empty(location{self.loc})"

'''test case'''
#have one solution
grid_setup = [
    Location(['E'], 10),
    Location(['N', 'W'], 11),
    Location(['S', 'E'], 12),
    Location(['N', 'E'], 13),
    Location(['E', 'W'], 21),
    Location(['S', 'E'], 22),
    Location(['N', 'E', 'W'], 23),
    Location(['N', 'S', 'E'], 31),
    Location(['N', 'S', 'E'], 32),
    Location(['N', 'S', 'E'], 33),
    Location(['W'], 34)
]
'''grid_setup = [#no solution
    Location(['E'], 10),
    Location(['S', 'E'], 11),
    Location(['N', 'S', 'E'], 12),
    Location(['S', 'W'], 13),
    Location(['S', 'E'], 21),
    Location(['S', 'E'], 22),
    Location(['S', 'E', 'W'], 23),
    Location(['N', 'S', 'W'], 31),
    Location(['N', 'S'], 32),
    Location(['N', 'S', 'E'], 33),
    Location(['W'], 34)
]'''
#grid has no solution
'''grid_setup = [
    Location(['E'], 10),
    Location(['E','W'],11),
    Location(['E', 'W'], 12),
    Location(['N', 'S'], 13),
    Location(['N', 'S'], 21),
    Location(['E','W'], 22),
    Location(['N','S'],23),
    Location(['N', 'S'], 31),
    Location(['N', 'S'], 32),
    Location(['N', 'S'], 33),
    Location(['W'], 34)]'''

'''if there are empty grid cell, this setup have 0 solution'''
def empty_grid_cell():
    #remove 21 and have 0 solution
    global grid_setup
    grid_setup=[
    Location(['E'], 10),
    Location(['N', 'W'], 11),
    Location(['S', 'E'], 12),
    Location(['N', 'E'], 13),
    Location(['S', 'E'], 22),#Location(['E', 'W'], 21),
    Location(['N', 'E', 'W'], 23),
    Location(['N', 'S', 'E'], 31),
    Location(['N', 'S', 'E'], 32),
    Location(['N', 'S', 'E'], 33),
    Location(['W'], 34)]
'''if there are STRAIGHT_PIPEs at certain location, this setup does not have a solution'''
def no_sol_with_row_strai():
    global grid_setup
    grid_setup = [
    Location(['E'], 10),
    Location(['N', 'S'], 11),
    Location(['N', 'S'], 12),
    Location(['N', 'S'], 13),
    Location(['N', 'E', 'W'], 21),
    Location(['N', 'E', 'W'], 22),
    Location(['N', 'E', 'W'], 23),
    Location(['N', 'E', 'W'], 31),
    Location(['N', 'S', 'E'], 32),
    Location(['N', 'S', 'E'], 33),
    Location(['W'], 34)]
    
#this is when at 10 and 11 is not connected at the beginning 
def disconnect_at_beginning():
    global grid_setup
    grid_setup = [
    Location(['E'], 10),
    Location(['N', 'W'], 11),
    Location(['S', 'E'], 12),
    Location(['N', 'E'], 13),
    Location(['E', 'W'], 21),
    Location(['S', 'E'], 22),
    Location(['N', 'E', 'W'], 23),
    Location(['N', 'S', 'E'], 31),
    Location(['N', 'S', 'E'], 32),
    Location(['N', 'S', 'E'], 33),
    Location(['W'], 34)
    ]
#if the entire grid is filled with angled pipes
def all_angled_pipe():
    global grid_setup
    grid_setup = [
    Location(['E'], 10),
    Location(['N', 'E'], 11),
    Location(['S', 'E'], 12),
    Location(['N', 'E'], 13),
    Location(['E', 'W'], 21),
    Location(['S', 'E'], 22),
    Location(['N', 'E'], 23),
    Location(['S', 'E'], 31),
    Location(['S', 'E'], 32),
    Location(['S', 'E'], 33),
    Location(['W'], 34)
    ]
    
#test for if the program can find two paths    
def two_path():
    global grid_setup
    grid_setup = [
    Location(['E'],10),
    Location(['S','E','W'],11),
    Location(['E','W'],12),
    Location(['S','W'],13),
    Location(['N','S'],21),
    Location(['E','W'],22),
    Location(['N','S'],23),
    Location(['N','E'],31),
    Location(['E','W'],32),
    Location(['N','E','W'],33),
    Location(['W'],34)    
    ]    
    
# Call your variables whatever you want
a = Location(['E'], 10)
b = Location(['W'], 34)

#stores all solutions
routes = []

def example_theory():
    '''check if any of the grid cell is empty, if it is not empty, remove from the list of location that is empty'''
    location_check=LOCATIONS.copy()
    for g in grid_setup:
        #remove the location that is not empty
        location_check.remove(g.location)
    for lc in location_check:
        #add constraint that the location is empty
        E.add_constraint(Empty(lc))
    '''find all location that is neighbours and store them in list NB'''
    '''first row neighbour'''#index for all location[10(0), 11(1), 12(2), 13(3), 21(4), 22(5), 23(6), 31(7), 32(8), 33(9), 34(10)]
    for l1 in LOCATIONS[:3]:#[10(0), 11(1), 12(2)]
        NB.append(NeighborLR(l1, l1 + 1))
    '''second row neighbour'''
    for l1 in LOCATIONS[4:6]:#[21, 22]
        NB.append(NeighborLR(l1, l1 + 1))
    '''third row neighbour'''
    for l1 in LOCATIONS[7:10]:#[31, 32]
        NB.append(NeighborLR(l1, l1 + 1))
    '''first column neighbour'''
    for l1 in LOCATIONS[1:4]:#[11, 12, 13]        
        NB.append(NeighborUD(l1, l1 + 10))
    '''second column neighbour'''
    for l1 in LOCATIONS[4:7]:#[21, 22, 23]
        NB.append(NeighborUD(l1, l1 + 10))
    #for all the location pair stored in NB, add constraint that they are neighbour
    E.add_constraint(And(NB))
    '''everthing other pair that is not in NB is not neighbour and since they are not neighbour, they are not connected'''
    for l1 in LOCATIONS:
        for l2 in LOCATIONS:
            if NeighborUD(l1, l2) not in NB and NeighborLR(l1, l2) not in NB:
                E.add_constraint(~NeighborUD(l1, l2)&~NeighborLR(l1, l2))
                E.add_constraint(~NeighborUD(l1, l2)>>~Connected(l1, l2)) 
                E.add_constraint(~NeighborLR(l1, l2)>>~Connected(l1, l2)) 
    '''if any of the location is empty in a neighbour pairs, then they are not connected to their neighbour'''
    for nb in NB:
        E.add_constraint((Empty(nb.loc1)|Empty(nb.loc2))>>(~Connected(nb.loc1, nb.loc2)&~Connected(nb.loc2, nb.loc1)))

    '''the opening of start piece can only facing east'''
    E.add_constraint(Location(['E'], 10))
    '''the opening of end piece can only facing west'''
    E.add_constraint(Location(['W'], 34))
    '''restict the pipe orientation at 10 and 34 so that no other pipe orietation can be at 10 and 34'''
    for p in PIPE_ORIENTATIONS:
        if  p!= ['E'] and p != ['W']:
            E.add_constraint(~Location(p, 10))
            E.add_constraint(~Location(p, 34))
    '''no other location can have pipe opening facing east or west'''
    for l in LOCATIONS[1:-1]:
        E.add_constraint(~Location(['E'], l))
        E.add_constraint(~Location(['W'], l))
    E.add_constraint(~Connected(10, 34)) #10 and 34 can't connect directly
    
    '''find all solution: there is a total of 6 solutions(found using a bfs algorithm)
    each solution has a distinct path travelled to get from 10 to 34
    each path will only consists of moving 4 times, from 11 to 33(starting from 11, and ending at 33) 
    connection for (10,11) and (33,34) is manually added
    have 2 loops and 1 mannual statement to find all the paths'''
    
    direction = [0,0,1,1] # 0 represents go right, 1 represents go down
    
    for i in range(3):
        route = []
        currPos = 11
        route.append(Connected(10,11))
        if i != 0:
            direction[i],direction[i+1] = direction[i+1],direction[i]
        for j in direction:
            if j == 0:
                route.append(Connected(currPos,currPos+1))
                currPos = currPos+1
            elif j == 1:
                route.append(Connected(currPos,currPos+10))
                currPos = currPos+10
        route.append(Connected(currPos,34))
        routes.append(route)
    
    for i in range(2):
        direction[i],direction[i+1] = direction[i+1],direction[i]
        route = []
        currPos = 11
        route.append(Connected(10,11))
        for j in direction:
            if j == 0:
                route.append(Connected(currPos,currPos+1))
                currPos = currPos+1
            elif j == 1:
                route.append(Connected(currPos,currPos+10))
                currPos = currPos+10
        route.append(Connected(currPos,34))
        routes.append(route)
        
    direction[1],direction[-1] = direction[-1],direction[1]
    route = []
    currPos = 11
    route.append(Connected(10,11))
    for j in direction:
        if j == 0:
            route.append(Connected(currPos,currPos+1))
            currPos = currPos+1
        elif j == 1:
            route.append(Connected(currPos,currPos+10))
            currPos = currPos+10
    route.append(Connected(currPos,34))
    routes.append(route)

    # print()
    #pprint(f"this is routes: {routes}")
    # print()
    '''for r in routes:
        print(r)'''
    
    '''enforce only one pipe per location except for 22'''
    for g in grid_setup:
        location=[]
        #enfore pipe orientation at 11 and 33
        if len(g.pipe) == 3:#enforce only 1 orientations for 3 opening pipe at different location
            if g.location == 11 or g.location == 12 or g.location == 13:#only want ['S','E','W'] in row 1
                '''(If there is a 3-opening pipe at location 11, it must have the orientation SEW. 
                Among the four possible orientations for a 3-opening pipe, only SEW can connect both downward and to the right, 
                with the remaining opening leading either downward or to the right.
                If a solution route passes through grid cell 11, the pipe must connect to the adjacent grid cell, whether to the right or below. 
                This specific pipe orientation is the only one that accommodates all potential directions the route might take. 
                If this orientation fails to establish the necessary connections, none of the other pipe orientations will work either.)'''
                E.add_constraint(~Location(['N', 'S', 'E'], g.location)&~Location(['N', 'S', 'W'], g.location)&~Location(['N', 'E', 'W'], g.location))
                E.add_constraint(Location(['S','E','W'],g.location)>>~Have_from_north(g.location))
            elif g.location == 33 or g.location == 32 or g.location == 31:#only want ['N', 'E', 'W'] in row 3
                E.add_constraint(~Location(['N', 'S', 'W'], g.location)&~Location(['S', 'E', 'W'], g.location)&~Location(['N','S', 'E'], g.location))
                E.add_constraint(Location(['N', 'E', 'W'],g.location)>>~Have_from_west(g.location))
            elif g.location == 21:#only want ['N','S','E'] at 21
                E.add_constraint(~Location(['N', 'S', 'W'], g.location)&~Location(['S', 'E', 'W'], g.location)&~Location(['N', 'E', 'W'], g.location))
                E.add_constraint(Location(['N','S','E'],g.location)>>~Have_from_west(g.location))
            elif g.location == 23:#only want ['N', 'S', 'W'] at 23
                E.add_constraint(~Location(['N', 'S', 'E'], g.location)&~Location(['S', 'E', 'W'], g.location)&~Location(['N', 'E', 'W'], g.location))
                E.add_constraint(Location(['N','S','W'],g.location)>>~Have_to_east(g.location))
            for p in THREE_OPENING_PIPE:
                location.append(Location(p, g.location))
            constraint.add_exactly_one(E, *location)
        elif g.pipe in STRAIGHT_PIPE:
            if g.location == 11 or g.location ==12 or g.location ==32 or g.location == 33 :#only want ['E', 'W'] at row 1 and row 3
                E.add_constraint(~Location(['N', 'S'], g.location))
                E.add_constraint(~Have_from_north(g.location)&~Have_to_south(g.location))
                if g.location == 11 or g.location == 12:
                    E.add_constraint(~Connected(g.location, g.location + 10))
            elif g.location == 21 or g.location == 23:#only want ['N', 'S'] at 21 and 23
                E.add_constraint(~Location(['E', 'W'], g.location))
                if g.location == 21:
                    E.add_constraint((Location(['E', 'W'],g.location)|Location(['N', 'S'],g.location))>>~Connected(g.location, g.location + 1))
                elif g.location == 23:
                    E.add_constraint((Location(['E', 'W'],g.location)|Location(['N', 'S'],g.location))>>~Connected(g.location, g.location - 1))
                E.add_constraint(Location(['N', 'S'],g.location)>>(~Have_to_east(g.location)&~Have_from_west(g.location)))
            elif g.location == 13:
                E.add_constraint(~Connected(g.location, g.location + 10))
            elif g.location == 31:
                E.add_constraint(~Connected(g.location, g.location +1))
            for p in STRAIGHT_PIPE:
                location.append(Location(p, g.location))
            constraint.add_exactly_one(E, *location)
        elif g.pipe in ANGLED_PIPE:
            if g.location == 11 or g.location == 12 or g.location == 13:#if there is angled pipe at row 1, it must oriented [S, W]
                E.add_constraint(~Location(['N', 'W'], g.location))
                E.add_constraint(~Location(['N', 'E'], g.location))
                E.add_constraint(~Location(['S', 'E'], g.location))
                E.add_constraint(~Have_from_north(g.location)&~Have_to_east(g.location))
                if g.location == 11 or g.location == 12:
                    E.add_constraint(~Connected(g.location, g.location + 1))
            elif g.location == 21:#if there is angled pipe at 21, it must oriented [N, E]
                E.add_constraint(~Location(['N', 'W'], g.location)&~Location(['S', 'W'], g.location)&~Location(['S', 'E'], g.location))
                E.add_constraint(~Connected(g.location, g.location + 10))
                E.add_constraint(~Have_from_west(g.location)&~Have_to_south(g.location))
            elif g.location == 23:#if there is angled pipe at 23, it must oriented [S, W]
                E.add_constraint(~Location(['N', 'W'], g.location)&~Location(['N', 'E'], g.location)&~Location(['S', 'E'], g.location))
                E.add_constraint(~Have_from_north(g.location)&~Have_to_east(g.location))
            elif g.location == 33 or g.location == 32 or g.location == 31:#if there is angled pipe at row 3, it must oriented [N, E]
                E.add_constraint(~Location(['N', 'W'], g.location))
                E.add_constraint(~Location(['S', 'W'], g.location))
                E.add_constraint(~Location(['S', 'E'], g.location))
                E.add_constraint(~Have_from_west(g.location)&~Have_to_south(g.location))
            for p in ANGLED_PIPE:#enforce 4 oreintation
                location.append(Location(p, g.location))
            constraint.add_exactly_one(E, *location)
    '''check location 22 after everthing other locaction has been checked'''
    for g in grid_setup:
        if g.location == 22:
            if g.pipe in STRAIGHT_PIPE:
                E.add_constraint((~Have_to_south(g.location-10)|~Have_from_north(g.location+10))>>~Location(['N', 'S'], g.location))
                E.add_constraint((~Have_to_east(g.location-1)|~Have_from_west(g.location+1))>>~Location(['E', 'W'], g.location))
                E.add_constraint((Have_to_south(g.location-10)&Have_from_north(g.location+10)&Have_to_east(g.location-1)&Have_from_west(g.location+1)&(~Connected(11,12)|~Connected(32,33)))>>~Location(['N', 'S'], g.location))
                E.add_constraint((Have_to_south(g.location-10)&Have_from_north(g.location+10)&Have_to_east(g.location-1)&Have_from_west(g.location+1)&(~Connected(11,21)|~Connected(23,33)))>>~Location(['E', 'W'], g.location))
                E.add_constraint(~Location(['E', 'W'], g.location)>>(~Connected(21, 22)&~Connected(22, 23)))
                E.add_constraint(~Location(['N', 'S'], g.location)>>(~Connected(12, 22)&~Connected(22, 32)))
            elif g.pipe in ANGLED_PIPE:
                E.add_constraint(~Location(['N', 'W'], g.location)&~Location(['S', 'E'], g.location))#prevent the pipe connect up and left
                E.add_constraint((~Have_to_south(12)|~Have_from_west(23))>>~Location(['N', 'E'], g.location))
                E.add_constraint((~Have_to_east(21)|~Have_from_north(32))>>~Location(['S', 'W'], g.location))
                E.add_constraint((Have_to_south(g.location-10)&Have_from_west(g.location+1)&Have_to_east(g.location-1)&Have_from_north(g.location+10)&(~Connected(11,21)|~Connected(32,33)))>>~Location(['S', 'W'], g.location))
                E.add_constraint((Have_to_south(g.location-10)&Have_from_west(g.location+1)&Have_to_east(g.location-1)&Have_from_north(g.location+10)&(~Connected(11,12)|~Connected(23,33)))>>~Location(['N', 'E'], g.location))
                E.add_constraint(~Location(['S', 'W'], g.location)>>(~Connected(21, 22)&~Connected(22, 32)))
                E.add_constraint(~Location(['N', 'E'], g.location)>>(~Connected(22, 23)&~Connected(12, 22)))
            elif g.pipe in THREE_OPENING_PIPE:#['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']
                E.add_constraint(~Have_from_north(32)>>(~Location(['N', 'S', 'E'], 22)&~Location(['N', 'S', 'W'],22)&~Location(['S', 'E', 'W'],22)))#['N', 'E', 'W']
                E.add_constraint(~Have_to_east(21)>>(~Location(['N', 'E', 'W'], 22)&~Location(['N', 'S', 'W'],22)&~Location(['S', 'E', 'W'],22)))#['N', 'S', 'E']
                E.add_constraint(~Have_from_west(23)>>(~Location(['N', 'S', 'E'], 22)&~Location(['S', 'E', 'W'],22)&~Location(['N', 'E', 'W'],22)))#['N', 'S', 'W']
                E.add_constraint(~Have_to_south(12)>>(~Location(['N', 'S', 'E'], 22)&~Location(['N', 'S', 'W'],22)&~Location(['N', 'E', 'W'],22)))#['S', 'E', 'W']
        else:
            continue
      
    E.add_constraint(And(*routes[0]) | And(*routes[1]) | And(*routes[2]) | And(*routes[3]) | And(*routes[4]) | And(*routes[5]))  
    
    #find two paths
    E.add_constraint((And(*routes[0]) | And(*routes[1])) | (And(routes[0]) | And(routes[2])) | (And(*routes[0]) | And(*routes[3]))
                     | (And(*routes[0]) | And(*routes[4])) | (And(*routes[0]) | And(*routes[5])) | (And(*routes[1]) | And(*routes[2]))
                     | (And(*routes[1]) | And(*routes[3])) | (And(*routes[1]) | And(*routes[4])) | (And(*routes[1]) | And(*routes[5]))
                     | (And(*routes[2]) | And(*routes[3])) | (And(*routes[2]) | And(*routes[3])) | (And(*routes[2]) | And(*routes[4]))
                     | (And(*routes[2]) | And(*routes[5])) | (And(*routes[3]) | And(*routes[4])) | (And(*routes[3]) | And(*routes[5]))
                     | (And(*routes[4]) | And(*routes[5])))
    return E

def display_solution(S, want=False):
    true_props = set()
    for k in S:
        if S[k] and (not want or 'Connected' in str(k)):
            true_props.add(str(k))
    print("\n".join(true_props))
if __name__ == "__main__":
    print() #to make it look cleaner
    '''model exploration'''
    #empty_grid_cell()
    #no_sol_with_row_strai()
    #two_path()
    print(grid_setup)
    T = example_theory()
    T = T.compile()
    S = T.solve()
    #pprint(f"what does S do?: \n{S}")
    if S:
        display_solution(S, True)
        print("there's a solution")
    else:
        print("No solution!!")
    # After compilation (and only after), you can check some of the properties
    # of your model:
    '''print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())'''

    '''print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))'''