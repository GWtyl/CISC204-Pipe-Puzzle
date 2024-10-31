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
    constraint.at_most(k)     
    