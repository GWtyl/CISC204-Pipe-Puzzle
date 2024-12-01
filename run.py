from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()
LOCATIONS = []
'''add location to LOCATIONS using loop from 10 to 34'''
for i in range(10, 35):
    LOCATIONS.append(i)
'''used to generate all possible orentations of a pipe'''
ORIENTATIONS = list('NSEW')

'''used to generate all possible orentations of a pipe'''
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

#TODO: may need to delete
'''possible pipe orientation for STRAIGHT piece'''
#STRAIGHT_PIPE = [['N', 'S'], ['E', 'W']]
'''possible pipe orientation for ANGLED piece'''
#ANGLED_PIPE = [['N', 'W'], ['N', 'E'], ['S', 'E'], ['S', 'W']]
'''possible pipe orientation for THREE_OPENING piece'''
#THREE_OPENING_PIPE = [['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]

# a visual representation of one grid cell
'''
     N
   +----+
 W |    | E
   +----+
     S   
'''

'''given pipe is at given location; this works for the setup'''
@proposition(E)
class Location(object): 
    def __init__(self, pipe, location) -> None:
        assert pipe in PIPE_ORIENTATIONS
        assert location in LOCATIONS
        self.pipe = pipe
        self.location = location
    def _prop_name(self):
        return f"({self.pipe} @ {self.location})"

'''the pipes at these location are connected'''
@proposition(E)
class Connected(object):
    def __init__(self, l1, l2) -> None:
        assert l1 in LOCATIONS
        assert l2 in LOCATIONS
        self.l1 = l1
        self.l2 = l2

    def _prop_name(self):
        return f"Connected({self.l1}, {self.l2})"
    
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
a = Location(['E'], '10')
b = Location(['W'], '34')
#c = Neighbor("c")
#d = BasicPropositions("d")
#e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")
'''test case'''
#have one solution
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

def example_theory():
    '''You should have some propositions representing if two squares are connected, 
    i.e. connected((x_1,y_1),(x_2,y_2)), or connected(a,b), depending on how you want to implement it. 
    Then, the condition for a solution being found is if there is a chain of "Trues" from the start to the end. 
    Essentially, you want connected(start, a_1) ∧ connected(a_1,a_2) ∧ ... ∧ connected(a_n, end). Here the a_i's are grid spaces. 
    If this expression evaluates to True (for some n) then you have a solution. Once you set up all the constraints and propositions, 
    checking this won't be too hard. You just need to write some code that checks all possible values of n to see if there is a path. 
    (For a 3x3 grid, n would be no larger than 9, for example, since if it was you would be doubling back on yourself; 
    in fact it's lower if you're only going down and to the right). '''

    '''# Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)'''
    #TODO: every location must have one pipe
    #TODO: to be neighbor, only 10 or 1 difference in location
    #TODO: To be connected, iff the pipe's opeing need to be facing each other and they are neighbours
    #NB(l1,l2)&'E'in Location(pipe,l1).pipe&'W' in Location(pipe,l1).pipe>>connected(l1,l2)
    #if NE on grid, check the other orientation of the same pipe
    #TODO: connected from 10 to 34 to be able to win: route 1 is (connected(start, a_1) ∧ connected(a_1,a_2) ∧ ... ∧ connected(a_n, end))
    #TODO: r1 or r2 or r3 or r4 or r5 or r6 using for loop to generate all possible routes
    #TODO:after rotating, mark it as visited/ check the connection before and after to make sure the rest is connected and the presvious has not changed
    #TODO: how to make sure it only connect to right and down
    #>>connectted(l1,l2)
    '''must have E at a location 10 and W at location 34'''
    E.add_constraint(a)
    E.add_constraint(b)
    '''start and end can not be connected directly'''
    E.add_constraint(~Connected(10, 34))



    return E

def display_solution(S, want=False):
    true_props = set()
    for k in S:
        if S[k] and (not want or '@' in str(k)):
            true_props.add(str(k)+' is '+str(S[k]))
    print("\n".join(true_props))
if __name__ == "__main__":
    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    #display_solution(T, True)
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
