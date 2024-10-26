
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
#import random
import random
# Encoding that will store all of your constraints
E = Encoding()

#ORIENTATIONS = list('NSEW')
#PIPE_TYPE = ['start', 'end' ,'p1', 'p2', 'p3']
LOCATIONS = ['10', '11' , '12', '13' , '21', '22', '23', '31', '32', '33', '34']
#PIPE_CONFIG = ['startE','endW']
PIPE_TYPE = [['E'],['W'],[['E'],['W']],[['E'],['W'],['S']]]#start...
CONNECTED = [[['E'],[['E'],['W']]],[[],[]]]
#win condition: go through neighbor array and make sure every pair of neighbor is connected
NEIGHBORUD = [['11','21'],['12','22'],['13','23'],['21','31'],['22','32'],['23','33']]

NEIGHBORLR = [['10','11'],['11','12'],['12','13'],['21','22'],['22','23'],['31','32'],
            ['32','33'],['33','34']]

for i in PIPE_TYPE:
    for j in i:
        if j == "E":
            for k in PIPE_TYPE:
                for a in k:
                    if a == "W":
                        c=[i,k]
                        CONNECTED.append(c)

            

CONNECT = [[['E'],['W']],[['N'],['S']]]
#TODO: model the oriatation and pipe type
for location in LOCATIONS:
    if(location):


NEIGHBOR = [['10','11'],[],[]]#...
Connect = [[['E'],['W']],[['N'],['S']]]
# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class Location(object): 
    def __init__(self, pipe, location) -> None:
        assert pipe in PIPE_TYPE
        assert location in LOCATIONS
        self.pipe = pipe_type
        self.location = location
    def _prop_name(self):
        return f"({self.pipe} @ {self.location})"

class Connected(object):
    
    def __init__(self, neighbor, pipe_type) -> None:
        assert neighbor in NEIGHBOR
        assert pipe_type in PIPE_TYPE
        self.pipe_type = pipe_type
        self.neighbor = neighbor
    def _prop_name(self):                    
        return f"({self.neighbor}@{self.location})"

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
#TODO: model the oriatation and pipe type
location_propositions = []
for l in LOCATIONS:
    pipe_name = [f'p{l}']
    if(l == '10'):
        location_propositions.append(Location(['E'], l))
    elif(l == '34'):
        location_propositions.append(Location(['W'], l))
    else:
        for i in range(len(PIPE_TYPE)):
            p=PIPE_TYPE[random.randint(0, len(PIPE_TYPE)-1)]
            location_propositions.append(Location(p, l))
    #constraint.add_exactly_one(E, location_propositions)
print(location_propositions)
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

    for i in range(0, len(ORIENTATIONS)):
        orien1 = PIPE_TYPE[i]
        for j in range(i + 1, len(ORIENTATIONS)):
            orien2 = PIPE_TYPE[j]

            pipe_type = [orien1, orien2]

    print(pipe_type)
