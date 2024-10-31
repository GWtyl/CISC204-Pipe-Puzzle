
from bauhaus import Encoding, proposition, constraint
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
class Neighbor(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[{self.loc1} --> {self.loc2}]"
@proposition(E)
class FancyPropositions(object):
    def __init__(self, data) -> None:
        assert data
    def _prop_name(self):
        return f"[data]"
# Call your variables whatever you want
a = Location(['E'],'10')# there must have a start piece at 10
b = Location(['W'],'34')# there must have a end piece at 34
c = FancyPropositions("c")
x = Location(['E'],'10')# there must have a start piece at 10
y = Location(['W'],'34')# there must have a end piece at 34
z = FancyPropositions("c")

# At least one of these will be true
#x,y,z

#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    
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
    #select one config; also made sure we have exactly one pipe on each location
    #[[E]@10]
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
    constraint.add_exactly_one(E, grid_setup)

    #all possible connection [E,[E,W]]
    '''possible_connectionsud = []
    for i in PIPE_TYPE:
        for j in i:
            if j == "S":
                for x in PIPE_TYPE:
                    for y in x:
                        if x == "N":
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
    constraint.add_exactly_one(E, possible_connectionslr)'''
    
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


    #TODO change the pipe1 and pipe2 to pipe in the grid_setup;
    # it means we need to chack every pair of neibour to see if they are connected
    #if they are connected, add them to constriant

    #write a connected function to check if two pipes are connected
    #to do this we have to do for 3 things 
    '''
    1. check if they are neighbors
    2. check if they are facing the same direction
    3. if these conditions are met put them into the  Connected list
    '''
    #this is only to check if they are connected and if they are beside eachother on the x axis(left and right)
    #first check the location to see if they are next to each other and the check if the pipe is facting the same directio

    #calls this function from twopipeconnection class to say two pipe is connected
    #TwoPipeConnection(pipe1,pipe2,location1,location2) 
    '''for nbor in NEIGHBORUD:
        if (nbor[0] in pipe1 and nbor[1] in pipe2):
            if "N" in pipe1 and "S" in pipe2:
                constraint.add_exactly_one.TwoPipeConnection(pipe1,pipe2,l1,l2)
        elif (nbor[0] in pipe2 and nbor[1] in pipe1):
            if "N" in pipe2 and "S" in pipe1:
                constraint.add_exactly_one(E,TwoPipeConnection(pipe1,pipe2,l1,l2))
    for i in range(0, len(grid_setup)):
        if  not pipe_connected(grid_setup[i], grid_setup[i+1]):
            break
    constraint.add_exactly_one(E,TwoPipeConnection(pipe1,pipe2,l1,l2))'''

    return E


if __name__ == "__main__":
    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
      
                  
    #print(possible_connectionsud)
    #print(len(location_propositions))
    #print(len(pos_for_11))

    #print(PIPE_TYPE)