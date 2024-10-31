
from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
#import random
import random
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
class striant(object):
    def __init__(self, pipe) -> None:
        assert pipe in PIPE_TYPE
        self.pipe = pipe

    def _prop_name(self):
        return f"PipeType({self.pipe})"
    
@proposition(E)
class Neighbor(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[{self.loc1} --> {self.loc2}]"


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
    E.add_constraint((~TwoPipeConnection(['W'], grid_setup[len(grid_setup)-1].pipe, '34', '33')&(Location(['N', 'S'],'33')))>>(Location(['E', 'W'],'33')))
    E.add_constraint((~TwoPipeConnection(['E'], grid_setup[0].pipe, '10', '11') & (Location(['N', 'S'], '11'))) >> (Location(['E', 'W'], '11')))
    E.add_constraint((~TwoPipeConnection(['E'], grid_setup[0].pipe, '10', '11') & (Location(['N', 'S'], '11'))) >> (Location(['E', 'W'], '11')))
    return E


if __name__ == "__main__":
    #[['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]
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
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    '''
    #E.introspect(T)

    
    #print(f"connect: {connected_pipe}")
    
    #print(len(location_propositions))
    #print(len(pos_for_11))
    #print(possible_connectionsud)
    #print(f"grid setup: {grid_setup}")