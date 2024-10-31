
import random


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
    
    connected_pipe = []
    #TODO change the pipe1 and pipe2 to pipe in the grid_setup;
    # it means we need to chack every pair of neibour to see if they are connected
    #if they are connected, add them to constriant
    #loop through UD and LR
    for i in range(0,len(grid_setup)-1):
        for connectLR in NEIGHBORLR:
            if connectLR[0] in grid_setup[i] and connectLR[1] in grid_setup[i+1]:
                connected_pipe.append(grid_setup[i])
                connected_pipe.append(grid_setup[i+1])
                break
            elif connectLR[0] in grid_setup[i+1] and connectLR[1] in grid_setup[i]:
                connected_pipe.append(grid_setup[i+1])
                connected_pipe.append(grid_setup[i])
                break
                
        for connectUD in NEIGHBORUD:
            if connectUD[0] in grid_setup[i] and connectUD[1] in grid_setup[i+1]:
                connected_pipe.append(grid_setup[i])
                connected_pipe.append(grid_setup[i+1])
                break
            elif connectUD[0] in grid_setup[i+1] and connectUD[1] in grid_setup[i]:
                connected_pipe.append(grid_setup[i+1])
                connected_pipe.append(grid_setup[i])