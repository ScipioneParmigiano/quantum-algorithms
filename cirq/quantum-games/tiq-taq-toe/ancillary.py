import cirq
import numpy as np

# player one settles with p=1, i.e the gate mutate the register from |0> to |1>
class G1Gate100(cirq.Gate):  
    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[0, 0, 1],
                         [1, 0, 0],
                         [0, 1, 0]])


    def _circuit_diagram_info_(self, args):
        return "[1]"

# player one occupies with p=1/2 two qubits, i.e the gate mutate the register from |0> to |1>
class G1Gate50(cirq.Gate):  
    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        a = 1/np.sqrt(2)
        return np.array([[a, a, 0],
                         [a, -a, 0],
                         [0, 0, 1]])

    def _circuit_diagram_info_(self, args):
        return "[0.5]"


# player two settles with p=1, i.e the gate mutate the register from |0> to |2>
class G2Gate100(cirq.Gate):  
    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[0, 0, 1],
                         [0, 1, 0],
                         [1, 0, 0]])


    def _circuit_diagram_info_(self, args):
        return "[2]"


# player two occupies with p=1/2 two qubits, i.e the gate mutate the register from |0> to |1>
class G2Gate50(cirq.Gate):  
    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        a = 1/np.sqrt(2)
        return np.array([[a, 0, a],
                         [0, 1, 0],
                         [a ,0, -a]])

    def _circuit_diagram_info_(self, args):
        return "[0.5]"


def map_coordinates_to_number(row, col):
    # maps the selected row and col values to the corresponding qutrit
    mapping = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }

    return mapping.get((row, col), None) - 1


def who_is_playing(player_circuit, qplayer):
    player_circuit.append(cirq.X(qplayer))
    player_circuit.append(cirq.measure(qplayer, key = "m"))
    sim = cirq.Simulator()
    result = sim.simulate(player_circuit)
    measurement = result.measurements["m"]

    if measurement== 0:
        print("player 1's turn:")
        current_player = "X"
    else:
        print("player 2's turn:")
        current_player = "0"
    return current_player, player_circuit


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_cells(cells):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    winners = []

    for condition in win_conditions:
        if cells[condition[0]] == cells[condition[1]] == cells[condition[2]] != 0:
            winners.append(cells[condition[0]])
    return winners


def print_occupied_cells(game):
    rows = [game[i:i+3] for i in range(0, 9, 3)]
    players = {1: 'X', 2: 'O'}

    for row in rows:
        print(" ".join([players[cell] if cell in players else '-' for cell in row]))



def get_input_col():
    col = input(f"enter columns (0-2): ")
    col = list(map(int, col.split()))
    if len(col) > 2 or len(col) == 0:
        print("You can't entangle more than one qutrit and at least one is required. \nPlease provide 1 or 2 numbers.\n")
        return get_input_col()
    else:
        return col


def get_input_row():
    row = input(f"enter rows (0-2): ")
    row = list(map(int, row.split()))
    if len(row) > 2 or len(row) == 0:
        print("You can't entangle more than one qutrit and at least one is required. \nPlease provide 1 or 2 numbers.\n")
        return get_input_row()
    else:
        return row


def update_circuit(circuit, qubits, current_player, r, c, nrow, ncol):
    # function that applies the correct gate to the correct qutrit
    if nrow == ncol and nrow == 1:
        if current_player == "X":
            index = map_coordinates_to_number(r, c)
            g = G1Gate100().on(qubits[index])
            circuit.append(g)

        if current_player == "0":
            index = map_coordinates_to_number(r, c)
            g = G2Gate100().on(qubits[index])
            circuit.append(g)
    else:    
        if current_player == "X":
            index = map_coordinates_to_number(r, c)
            g = G1Gate50().on(qubits[index])
            circuit.append(g)

        if current_player == "0":
            index = map_coordinates_to_number(r, c)
            g = G2Gate50().on(qubits[index])
            circuit.append(g)


def check_winner(still_empty_cells, circuit, qubits):
    # once every cell is full, this function check if we have a winner or not and
    # who is the winner
    if still_empty_cells != 0:
        return False, None, None
    else:
        # add measurements to the circuit
        circuit.append(cirq.measure(qubits, key = "M"))

        sim = cirq.Simulator()
        result = sim.simulate(circuit)
        measurement = result.measurements["M"]
        winners = check_cells(measurement)
        
        return True, winners, measurement