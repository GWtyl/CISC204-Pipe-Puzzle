from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
import random
# Encoding that will store all of your constraints
E = Encoding()
LOCATIONS = [10, 11, 12, 13, 21, 22, 23, 31, 32, 33, 34]
NB = []
can_be_connected_pipe = []
'''LOCATION_xy= []
def setup_grid_location(x,y):#x is row, y is column#x:3, y:3
    assert x < 4 and y < 4
    for x in range(1,y+1):
        for y in range(1,x+1):
            LOCATIONS.append(f"{x}{y}")
            LOCATION_xy.append([x,y])'''

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
STRAIGHT_PIPE = [['N', 'S'], ['E', 'W']]
'''possible pipe orientation for ANGLED piece'''
ANGLED_PIPE = [['N', 'W'], ['N', 'E'], ['S', 'E'], ['S', 'W']]
'''possible pipe orientation for THREE_OPENING piece'''
THREE_OPENING_PIPE = [['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]

# a visual representation of one grid cell
'''
     N
   +----+
 W |    | E
   +----+
     S   
'''
'''the type of pipe(straight, angled, three_opening) can opens to these orientations'''
#TODO:may not use this; may need to delete
@proposition(E)
class Straight_Pipe(object): 
    def __init__(self, pipe_specific) -> None:
        assert pipe_specific in STRAIGHT_PIPE
        self.pipe_specific = pipe_specific
    def _prop_name(self):
        return f"(opens {self.pipe_specific})"
@proposition(E)
class Angled_Pipe(object): 
    def __init__(self, pipe_specific) -> None:
        assert pipe_specific in ANGLED_PIPE
        self.pipe_specific = pipe_specific
    def _prop_name(self):
        return f"(opens{self.pipe_specific})"

@proposition(E)
class Three_Opening_Pipe(object): 
    def __init__(self,pipe_specific) -> None:
        assert pipe_specific in THREE_OPENING_PIPE
        self.pipe_specific = pipe_specific
    def _prop_name(self):
        return f"(opens {self.pipe_specific})"
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
'''pipe are connected to each other left to right'''
@proposition(E)
class Pipe_ConnectLR(object):
    def __init__(self, pipe1, pipe2) -> None:
        assert pipe1 in PIPE_ORIENTATIONS
        assert pipe2 in PIPE_ORIENTATIONS
        self.pipe1 = pipe1
        self.pipe2 = pipe2

    def _prop_name(self):
        return f"[Pipe_ConnectLR({self.pipe1}, {self.pipe2})]"  
'''pipe are connected to each other up and down'''
@proposition(E)
class Pipe_ConnectUD(object):
    def __init__(self, pipe1, pipe2) -> None:
        assert pipe1 in PIPE_ORIENTATIONS
        assert pipe2 in PIPE_ORIENTATIONS
        self.pipe1 = pipe1
        self.pipe2 = pipe2

    def _prop_name(self):
        return f"[Pipe_ConnectUD({self.pipe1}, {self.pipe2})]"
'''given two locations are neighbors (they are beside each other)'''
@proposition(E)
class NeighborLR(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[NeighborLR({self.loc1}, {self.loc2})]"
'''given two locations are neighbors (they are on top of each other)'''
@proposition(E)
class NeighborUD(object):
    def __init__(self, loc1, loc2) -> None:
        assert loc1 in LOCATIONS
        assert loc2 in LOCATIONS
        self.loc1 = loc1
        self.loc2 = loc2

    def _prop_name(self):
        return f"[NeighborUD({self.loc1}, {self.loc2})]"
'''the location is occupied(not empty)'''
@proposition(E)
class Not_empty(object):
    def __init__(self, loc) -> None:
        assert loc in LOCATIONS
        #assert [loc1,loc2] in NEIGHBORUD or [loc1,loc2] in NEIGHBORLR, f"Invalid connection: {loc1} and {loc2}"
        self.loc = loc

    def _prop_name(self):
        return f"[Not_empty({self.loc})]"
'''Pipe orientation connected down'''
'''@proposition(E)
class Pipe_down(object):
    def __init__(self, pipe) -> None:
        assert pipe in PIPE_ORIENTATIONS
        self.pipe = pipe

    def _prop_name(self):
        return f"[Pipe_connect_down({self.pipe})]"'''
'''Pipe orientation connected right'''
'''@proposition(E)
class Pipe_right(object):
    def __init__(self, pipe) -> None:
        assert pipe in PIPE_ORIENTATIONS
        self.pipe = pipe

    def _prop_name(self):
        return f"[Pipe_connect_right({self.pipe})]"'''
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

# Call your variables whatever you want
a = Location(['E'], 10)
b = Location(['W'], 34)
#c = Neighbor("c")
#d = BasicPropositions("d")
#e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")

def example_theory():
    '''You should have some propositions representing if two squares are connected, 
    i.e. connected((x_1,y_1),(x_2,y_2)), or connected(a,b), depending on how you want to implement it. 
    Then, the condition for a solution being found is if there is a chain of "Trues" from the start to the end. 
    Essentially, you want connected(start, a_1) ∧ connected(a_1,a_2) ∧ ... ∧ connected(a_n, end). Here the a_i's are grid spaces. 
    If this expression evaluates to True (for some n) then you have a solution. Once you set up all the constraints and propositions, 
    checking this won't be too hard. You just need to write some code that checks all possible values of n to see if there is a path. 
    (For a 3x3 grid, n would be no larger than 9, for example, since if it was you would be doubling back on yourself; 
    in fact it's lower if you're only going down and to the right). '''
    #TODO: how to prevent the pipe from leads to outside of the grid
    E.add_constraint(~Pipe_ConnectLR(['E'], ['W']))
    #add can_be_connected pipe
    for p in PIPE_ORIENTATIONS:
        for q in PIPE_ORIENTATIONS:
            if 'E' in p and 'W' in q:
                can_be_connected_pipe.append(Pipe_ConnectLR(p, q))
            elif 'N' in p and 'S' in q:
                can_be_connected_pipe.append(Pipe_ConnectUD(p, q))
    '''for p in can_be_connected_pipe:
        print(p)'''
    #E.add_constraint(And(can_be_connected_pipe))
    for p in PIPE_ORIENTATIONS:
        for q in PIPE_ORIENTATIONS:
            if Pipe_ConnectLR(p, q) not in can_be_connected_pipe and Pipe_ConnectUD(p, q) not in can_be_connected_pipe:
                E.add_constraint(~Pipe_ConnectLR(p, q))
                E.add_constraint(~Pipe_ConnectUD(p, q))
    '''must have E at a location 10 and W at location 34'''
    E.add_constraint(a)
    E.add_constraint(b)
    '''start and end can not be connected directly'''
    E.add_constraint(~Connected(10, 34))
    for p in STRAIGHT_PIPE:
        E.add_constraint(Straight_Pipe(p))
    for p in ANGLED_PIPE:
        E.add_constraint(Angled_Pipe(p))
    for p in THREE_OPENING_PIPE:
        E.add_constraint(Three_Opening_Pipe(p))

    for g in grid_setup:
        if g.pipe in STRAIGHT_PIPE:
            E.add_constraint(Straight_Pipe(g.pipe)>>(Location(['N', 'S'], g.location)|Location(['E', 'W'], g.location)))
        if g.pipe in ANGLED_PIPE:
            E.add_constraint(Angled_Pipe(g.pipe)>>(Location(['N', 'W'], g.location)|Location(['N', 'E'], g.location)|Location(['S', 'E'], g.location)|Location(['S', 'W'], g.location)))
        if g.pipe in THREE_OPENING_PIPE:
            E.add_constraint(Three_Opening_Pipe(g.pipe)>>(Location(['N', 'S', 'E'], g.location)|Location(['N', 'S', 'W'], g.location)|Location(['N', 'E', 'W'], g.location)|Location(['S', 'E', 'W'], g.location)))
    '''check what location have pipe'''
    for l in LOCATIONS:
        for g in grid_setup:
            if g.location == l:
                E.add_constraint(Not_empty(l))
    '''first row neighbour'''#[10(0), 11(1), 12(2), 13(3), 21(4), 22(5), 23(6), 31(7), 32(8), 33(9), 34(10)]
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
    E.add_constraint(And(NB))
    '''everthing else is not neighbour and since they are not neighbour, they are not connected'''
    for l1 in LOCATIONS:
        for l2 in LOCATIONS:
            if NeighborUD(l1, l2) not in NB and NeighborLR(l1, l2) not in NB:
                E.add_constraint(~NeighborUD(l1, l2)&~NeighborLR(l1, l2))
                E.add_constraint(~Connected(l1, l2))

    #TODO: To be connected, iff the pipe's opeing need to be facing each other and they are neighbours
    #NB(l1,l2)&'E'in Location(pipe,l1).pipe&'W' in Location(pipe,l1).pipe>>connected(l1,l2)
    #if NE on grid, check the other orientation of the same pipe
    for g1 in grid_setup:#Location(pipe,l1)
        for g2 in grid_setup:
                E.add_constraint((Not_empty(g1.location)&Not_empty(g2.location)&NeighborLR(g1.location,g2.location)&Pipe_ConnectLR(g1.pipe,g2.pipe))>>Connected(g1.location,g2.location))
                E.add_constraint((Not_empty(g1.location)&Not_empty(g2.location)&NeighborUD(g1.location,g2.location)&Pipe_ConnectUD(g1.pipe,g2.pipe))>>Connected(g1.location,g2.location))
    #TODO: connected from 10 to 34 to be able to win: route 1 is (connected(start, a_1) ∧ connected(a_1,a_2) ∧ ... ∧ connected(a_n, end))
    '''this out put[Connected(10, 11), Connected(11, 12), Connected(12, 13), Connected(13, 23), Connected(21, 22), Connected(22, 23), Connected(23, 33), Connected(31, 32), Connected(32, 33), Connected(33, 34)]
    [Connected(11, 21), Connected(12, 22), Connected(21, 31), Connected(22, 32)]'''
    '''possible_route=[]
    for i in range(len(LOCATIONS)):#[10, 11, 12, 13, 21, 22, 23, 31, 32, 33, 34]
        for j in range(i+1,len(LOCATIONS)):#[11, 12, 13, 21, 22, 23, 31, 32, 33, 34]
            if (NeighborLR(LOCATIONS[i], LOCATIONS[j]) in NB or NeighborUD(LOCATIONS[i], LOCATIONS[j]) in NB)and (Connected(LOCATIONS[i], LOCATIONS[j]) not in possible_route):
                possible_route.append(Connected(LOCATIONS[i], LOCATIONS[j]))
    #print(possible_route)'''
    #TODO: make SAT solver to find the route
    def find_routes(start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        routes = []
        for loc in LOCATIONS:
            if loc not in path:
                if NeighborLR(start, loc) in NB or NeighborUD(start, loc) in NB:
                    new_routes = find_routes(loc, end, path)
                    for new_route in new_routes:
                        routes.append(new_route)
        return routes

    routes = find_routes(10, 34)
    route_constraints = []
    for route in routes:
        route_constraint = And([Connected(route[i], route[i+1]) for i in range(len(route)-1)])
        route_constraints.append(route_constraint)

    E.add_constraint(Or(route_constraints))
    '''E.add_constraint((Connected(10, 11)&Connected(11, 21)&Connected(21, 31)&Connected(31, 32)&Connected(32, 33)&Connected(33, 34))|
                     (Connected(10, 11)&Connected(11, 12)&Connected(12, 13)&Connected(13, 23)&Connected(23, 33)&Connected(33, 34))|
                     (Connected(10, 11)&Connected(11, 12)&Connected(12, 22)&Connected(22, 32)&Connected(32, 33)&Connected(33, 34))|
                    (Connected(10, 11)&Connected(11, 21)&Connected(21, 22)&Connected(22, 32)&Connected(32, 33)&Connected(33, 34)))'''

    #find all possible routes between 10 to 34 and add them to the list but thee location should be consistent with the grid like after Conncted[10,11] should be [11,12] or [11,21]




    #TODO: r1 or r2 or r3 or r4 or r5 or r6 using for loop to generate all possible routes
    #TODO:?after rotating, mark it as visited/ check the connection before and after to make sure the rest is connected and the presvious has not changed
    #TODO: how to make sure it only connect to right and down
    



    return E

def display_solution(S, want=False):
    true_props = set()
    for k in S:
        if S[k] and (not want or 'Connected' in str(k)):
            true_props.add(str(k))
    print("\n".join(true_props))
if __name__ == "__main__":
    #[['W'], ['E'], ['N', 'S'], ['N', 'E'], ['N', 'W'], ['S', 'E'], ['S', 'W'], ['E', 'W'], ['N', 'S', 'E'], ['N', 'S', 'W'], ['N', 'E', 'W'], ['S', 'E', 'W']]
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
    '''print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())'''

    '''print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))'''
