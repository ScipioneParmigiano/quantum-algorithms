# Tiq toq toe: quantum version of the classical tic-tac-toe

# Command line interface game where two players who take turns marking the spaces 
# in a three-by-three grid with X or O. The player who succeeds in placing three 
# of their marks in a horizontal, vertical, or diagonal row is the winner. 

# This version of the game is different from the classical one because it makes use
# of Google's quantum computing framework 'cirq', allowing players to make non-classical move,
# i.e. to place more than one X or 0 in a single turn. Such Xs or 0s are then entangled and 
# once measured they will collapse, resulting in a single X or 0.
######################################
#           #             #          #   
#     00    #     01      #    02    # 
#           #             #          # 
######################################
#           #             #          # 
#     10    #     11      #    12    # 
#           #             #          # 
######################################
#           #             #          #  
#     20    #     21      #    22    #   
#           #             #          # 
######################################

import cirq
import numpy as np
from ancillary import * 
import time
import os

# we have a qubit representing which player is playing:
#  - |0> stands for player 1
#  - |1> stands for player 2
#
# and we have 9 qutrit register representing the state of a single
# cell of the board: 
# - |0> stands for empty cell;
# - |1> stands for player1"s cell 
# - |2> stands for player2"s cell


def play_game():
    # board is used to check if a cell was already occupied
    board = [[' ' for _ in range(3)] for _ in range(3)]

    # X is player 1, 0 is player 2
    players = ['X', 'O']

    # still_empty_cells is used to terminate the game once its value becomes 0, in fact
    # unlike traditional tic tac toe, this game continues untill there is no cell left,
    # then it measure the circuit and assert if someone has won
    still_empty_cells = 9 

    # player 2d circuit
    player_circ = cirq.Circuit()
    qplayer = cirq.NamedQubit("player")
    player_circ.append(cirq.X(qplayer))

    # board 3d circuit
    qubits = cirq.GridQid.rect(3, 3, dimension=3)
    circuit = cirq.Circuit()

    while still_empty_cells != 0:
        # set current player
        print_board(board)
        current_player, player_circ = who_is_playing(player_circ, qplayer)

        # input from current_player
        row = get_input_row()
        col = get_input_col()
        
        for r in list(row):
            for c in list(col):
                if board[r][c] == ' ':
                    board[r][c] = current_player
                    still_empty_cells -= 1

                    # update qutrits register
                    update_circuit(circuit, qubits, current_player, r, c, len(row), len(col))

                    # check if no cell is empty and return the winner 
                    end_game, winners, measurement = check_winner(still_empty_cells, circuit, qubits)                  
                    
                    if end_game:  
                        os.system('clear')
                        print_occupied_cells(measurement)
                        print(f"\nAnd the winner is/are: {winners}")
                        break

                else:
                    print("That position is already taken. Try again.\n")
                    
                    # X gate so that it's again the player who made a mistake to play 
                    player_circ.append(cirq.X(qplayer))
                    time.sleep(0.5)


if __name__ == "__main__":
    play_game()
