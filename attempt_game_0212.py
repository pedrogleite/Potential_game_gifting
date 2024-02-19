import numpy as np
import matplotlib.pyplot as plt

def potential_matrices(size, param1, param2):
        player1_potential_matrix = np.array([[param1, 0],
                                             [0, size - param1]])

        player2_potential_matrix = np.array([[param2, 0],
                                             [0, size - param2]])
        
        return player1_potential_matrix, player2_potential_matrix

def play_game(size, r, gift):
    datax = []
    datay = []
    
    # Write payoff matix
    actual_payoff_matrix = np.array([[(2, 2), (r, 1)],
                                     [(1, r), (1, 1)]])
    
    for param1 in range(1, size):     # param_1 represents how much gifting player 1 can affort
        for param2 in range(1, size): # param_2 represents the % that player 2 wants to hunt rather than forage

            player1_potential_matrix, player2_potential_matrix = potential_matrices(size, param1, param2)

            count = 0
            start = False
            finish = False
            while True:
                
                # Choose strategy based on the potential matrix
                player1_strategy = np.unravel_index(np.argmax(player1_potential_matrix), player1_potential_matrix.shape)[0]
                player2_strategy = np.unravel_index(np.argmax(player2_potential_matrix), player2_potential_matrix.shape)[1]

                if (player1_potential_matrix[0, 0] <= gift - r) and (not finish): # Make player1 hunt if it knows that player2 will hunt
                    player1_strategy = 1
                elif finish:
                    player1_strategy = 0

                player1_payoff, player2_payoff = actual_payoff_matrix[player1_strategy, player2_strategy]

                player2_potential_matrix[player2_strategy, player2_strategy] = player2_potential_matrix[player2_strategy, player2_strategy] + player2_payoff # Player2 gets regular payoff

                player1_potential_matrix[player1_strategy, player1_strategy] = player1_potential_matrix[player1_strategy, player1_strategy] + player1_payoff - gift # Player1 loses gift amount
                player2_potential_matrix[0, 0] = player2_potential_matrix[0, 0] + gift # Player2 receives gift favoring the prosocial equilibrium


                if player2_strategy == 0: # 'start' allows player1 to know when player2 first hunted to guess the next time it will hunt again
                    start = True 

                if start:
                    count += 1

                    if (np.isclose(count, np.ceil(((-r - gift)/(gift - actual_payoff_matrix[0][1][1])))) or gift >= (-r)): # checks whether player2 will hunt next time
                        finish = True
                
                if (player1_strategy == 0 and player2_strategy == 0): # ends the game if both players hunt, marks as success
                    datax.append(param1)
                    datay.append(param2)
                    break

                if (player1_potential_matrix[0][0] < 1) or (player1_potential_matrix[1][1] < 1):  # end the game if player1's potential goes equal to or less than 1
                    break

    probability_prosocial = len(datax)/size**2 # writes the percentage of successes over 'size' amount of runs.
    return probability_prosocial, datax, datay

def p1_p2_plot(size, r, gift):
    _, datax, datay = play_game(size, r, gift)

    plt.scatter(100*np.array(datax)/size, 100*np.array(datay)/size, color='green')
    plt.xlabel("Player 1's Initial Potential to Hunt [%]")
    plt.ylabel("Player 2's Initial Potential to Hunt [%]")
    plt.title(f'Convergence to Prosocial Equilibrium \n as a Function of Initial Potential Towards Hunting \n with r = {r} and $\\gamma$ = {gift}:  {100*len(datax)/size**2:.1f}%')
    plt.xlim(0,100)
    plt.ylim(0,100)
    plt.show()
p1_p2_plot(100, -6, 10) 
