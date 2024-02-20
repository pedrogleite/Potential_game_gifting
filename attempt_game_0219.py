import numpy as np
import matplotlib.pyplot as plt

def potential_matrices(size, param1, param2):
        p1_potential_matrix = np.array([[param1, 0], 
                                             [0, size - param1]])

        p2_potential_matrix = np.array([[param2, 0],
                                             [0, size - param2]])
        
        return p1_potential_matrix, p2_potential_matrix

def play_game(size, r, gift):
    datax = []
    datay = []

    actual_payoff_matrix = np.array([[(2, 2), (r, 1)],
                                     [(1, r), (1, 1)]])
    
    for param1 in range(1, size):     # param_1 represents how much gifting player 1 can affort
        for param2 in range(1, size): # param_2 represents the % that player 2 wants to hunt rather than forage

            p1_potential_matrix, p2_potential_matrix = potential_matrices(size, param1, param2)

            count = 0
            start = False
            finish = False
            knows_hunt = False     # it needs to know_hunt and know_forage to know that hunting is preffered. Otherwise, it doesn't know that gifting is good.
            knows_forage = False
            hunts = 0
            while True:
                
                # Choose strategy based on the potential matrix
                p1_hunt_chance = p1_potential_matrix[0][0] / (p1_potential_matrix[0][0] + p1_potential_matrix[1][1])
                p2_hunt_chance = p2_potential_matrix[0][0] / (p2_potential_matrix[0][0] + p2_potential_matrix[1][1])
                
                p1_strategy = np.random.choice([0, 1], p = [p1_hunt_chance, 1 - p1_hunt_chance])
                p2_strategy = np.random.choice([0, 1], p = [p2_hunt_chance, 1 - p2_hunt_chance])


                if (knows_forage == False) and (p1_strategy == 1) and (p2_strategy == 1):
                    knows_forage == True

                if (knows_hunt == False) and (p1_strategy == 0) and (p2_strategy == 0):
                    knows_hunt == True                

                p1_payoff, p2_payoff = actual_payoff_matrix[p1_strategy, p2_strategy]

                p2_potential_matrix[p2_strategy, p2_strategy] = p2_potential_matrix[p2_strategy, p2_strategy] + p2_payoff 

                if knows_hunt and knows_forage:
                    p1_potential_matrix[p1_strategy, p1_strategy] = p1_potential_matrix[p1_strategy, p1_strategy] + p1_payoff - gift  # plays whatever strategy it chooses, subtracts the gift that is always shared
                    p2_potential_matrix[0, 0] = p2_potential_matrix[0, 0] + gift # receives gift favoring the prosocial equilibrium
                else:
                    p1_potential_matrix[p1_strategy, p1_strategy] = p1_potential_matrix[p1_strategy, p1_strategy] + p1_payoff

                if (p1_strategy == 0 and p2_strategy == 0):
                    hunts += 1                              # adds a point every time both players hunt
                    if hunts == 3:
                        datax.append(param1)
                        datay.append(param2)
                        break

                # if (p1_strategy != 0) or (p2_strategy != 0):    # this makes it such that the players have to hunt 'hunts' times in a row for it to succeed
                #     hunts = 0

                if (p1_potential_matrix[0][0] < 1) or (p1_potential_matrix[1][1] < 1) or (p2_potential_matrix[0][0] < 1) or (p2_potential_matrix[1][1] < 1):
                    break

    return datax, datay

def p1_p2_plot(size, r, gift):
    datax, datay = play_game(size, r, gift)

    plt.scatter(100*np.array(datax)/size, 100*np.array(datay)/size, color='green')
    plt.xlabel("Player 1's Initial Potential to Hunt [%]")
    plt.ylabel("Player 2's Initial Potential to Hunt [%]")
    plt.title(f'Convergence to Prosocial Equilibrium \n as a Function of Initial Potential Towards Hunting \n with r = {r} and $\\gamma$ = {gift}:  {100*len(datax)/size**2:.1f}%')
    plt.xlim(0,100)
    plt.ylim(0,100)
    plt.show()

p1_p2_plot(100, -6, 10)    
