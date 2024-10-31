
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

CONNECTED = []
for i in PIPE_TYPE:
    for j in i:
        if j == "S":
            for x in PIPE_TYPE:
                for y in x:
                    if x == "N":
                        c=[i,x]
                        CONNECTED.append(c)    
        else:
            break  #check: only break 1 loop
for i in PIPE_TYPE:
    for j in i:
        if j == "E":
            for k in PIPE_TYPE:
                for a in k:
                    if a == "W":
                        c=[i,k]
                        CONNECTED.append(c)
CONNECTED.remove([['E'], ['W']])

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class Location(object): 
    def __init__(self, pipe, location) -> None:
        assert pipe in PIPE_TYPE
        assert location in LOCATIONS
        self.pipe = pipe
        self.location = location
    def _prop_name(self):
        return f"({self.pipe} @ {self.location})"
    
#TODO: get the setup and check if two pipe is connected and then put them into TODO checked list
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
        return f"({self.pipe1}@{self.location1} -> {self.edge2}@{self.location1})"

   
#model the oriatation and pipe type
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
    #@constraint.at_most_k(E, 11)   
   

# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = FancyPropositions("a") #connected
b = FancyPropositions("b") #
c = FancyPropositions("c")
d = FancyPropositions("d")
e = FancyPropositions("e")
a = FancyPropositions("a") #connected
b = FancyPropositions("b") #
c = FancyPropositions("c")
d = FancyPropositions("d")
e = FancyPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E

#TODO: write a connected function to check if two pipes are connected
#to do this we have to do for 3 things 
'''
1. check if they are neighbors
2. check if they are facing the same direction
3. if these conditions are met put them into the  Connected list
'''
#this is only to check if they are connected and if they are beside eachother on the x axis(left and right)
#first check the location to see if they are next to each other and the check if the pipe is facting the same direction
def pipe_connected(pipe1, pipe2):
    
    #calls this function from twopipeconnection class to check if the location and pipe exists
    #TwoPipeConnection.__init__(pipe1,pipe2,location1,location2) 
    
    for nbor in NEIGHBORLR:
        
        #check if they are neighbor ( neighbor is always counted from left to right) 
        if (nbor[0] in pipe1 and nbor[1] in pipe2):
            if "E" in pipe1 and "W" in pipe2:
                return True
        elif (nbor[0] in pipe2 and nbor[1] in pipe1):
            if "E" in pipe2 and "W" in pipe1:
                return True
            
    for nbor in NEIGHBORUD:
        if (nbor[0] in pipe1 and nbor[1] in pipe2):
            if "N" in pipe1 and "S" in pipe2:
                return True
        elif (nbor[0] in pipe2 and nbor[1] in pipe1):
            if "N" in pipe2 and "S" in pipe1:
                return True
    return False
  
  
#(["N","E","S"] @ 3.3) 
def win_condition(grid_setup):
    for i in range(0, len(grid_setup)):
        if  not pipe_connected(grid_setup[i], grid_setup[i+1]):
            return False
    
    return True

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
    print()
    ORIENTATIONS = list('NSEW')

    '''for i in range(0, len(ORIENTATIONS)):
        orien1 = PIPE_TYPE[i]
        for j in range(i + 1, len(ORIENTATIONS)):
            orien2 = PIPE_TYPE[j]

            PIPE_TYPE = [orien1, orien2]'''

    #print(PIPE_TYPE)
    #print(len(location_propositions))
    #print(CONNECTED)

