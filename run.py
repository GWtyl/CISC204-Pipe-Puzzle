
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

#ORIENTATIONS = list('NSEW')
#PIPE_TYPE = ['start', 'end' ,'p1', 'p2', 'p3']
LOCATIONS = ['10', '11' , '12', '13' , '21', '22', '23', '31', '32', '33', '34']
#PIPE_CONFIG = ['startE','endW']
PIPE_TYPE = [['E'],[['E'],['W']],[['E'],['W'],['S']]]#start...
CONNECTED = [[['E'],[['E'],['W']]],[[],[]]]
#win condition: go through neighbor array and make sure every pair of neighbor is connected
NEIGHBOR = [['10','11'],[],[]]#...
A = [[['E'],['W']],[['N'],['S']]]
#testtest

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class Configuration(object): 

    def __init__(self, pipe_type, location) -> None:
        assert pipe_type in PIPE_TYPE
        assert location in LOCATIONS
        self.pipe = pipe_type
        self.location = location
    def _prop_name(self):
        return f"({self.pipe_type} @ {self.location})"

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

# Call your variables whatever you want
a = BasicPropositions("a") #connected
b = BasicPropositions("b") #
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
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
