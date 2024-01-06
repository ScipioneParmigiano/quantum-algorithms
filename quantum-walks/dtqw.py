# Discrete time quantum walk as in http://refhub.elsevier.com/S1574-0137(21)00059-9/sb45

# let H_c the Hilbert space spanned by the two basis state |0> and |1> representing forward and backward progression on a line graph
# let H_s the Hilbert space used to encode the position of the walker
# the state of all possible outcome is given by H_c ⊗ H_s 

# let the operator U to evolve the walk at each step, defined as:
# U = |0><1| ⊗ (\sum |j+1><j| + \sum |j-1><j|)

# I use Hadamard gate s.t. the probability of moving forward equals the probability of moving backward, hence
# the operator that evolves the system is: E = U(H ⊗ I) where I is the identity matrix

import cirq
import matplotlib.pyplot as plt
import numpy as np 

def quantum_walk(evolution_operator, initialization_function, number_qubits, n_iter=10, n_sample=50):
    '''
        - evolution_operator is what above I called E;
        - initialization_function is a function tha t applies the necessary gates to initialize the coin and the walker;
        - number_qubits is the number of qubits.
    '''
    # setup
    qubits = cirq.LineQubit.range(number_qubits+1)
    circuit = cirq.Circuit()

    # init
    initialization(circuit, qubits, number_qubits)

    # steps
    for j in range(n_iter):
        evolution_operator(circuit, qubits, number_qubits)
    
    circuit.append(cirq.measure(*qubits[:-1], key="m"))

    # print(circuit)
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions = n_sample)
    hist = result.histogram(key="m")

    return hist, result


def step(circuit, qubits, number_qubits):
    '''
        function that flips the coin. Requires:
        - the circuit we are working on;
        - the qubits we are using.
    '''

    # H on the coin
    circuit.append(cirq.H(qubits[number_qubits]))
  
    # Addition operator
    circuit.append(cirq.X.on(qubits[number_qubits]))

    for i in range(number_qubits, 0, - 1):
        controls = [cirq.LineQubit(v) for v in range(number_qubits, i-1, -1)]

        circuit.append(cirq.X.on(cirq.LineQubit(i-1)).controlled_by(*controls))
        if (i > 1):
            circuit.append(cirq.X.on(cirq.LineQubit(i-1)))

    circuit.append(cirq.X.on(cirq.LineQubit(number_qubits)))

    # Subtraction operator
    for i in range(1, number_qubits + 1):
        controls = [cirq.LineQubit(v) for v in range(number_qubits, i-1, -1)]

        circuit.append(cirq.X.on(cirq.LineQubit(i-1)).controlled_by(*controls))
        if (i < number_qubits):
            circuit.append(cirq.X.on(cirq.LineQubit(i)))


def graph(hist):
    x_arr = list(hist.keys())
    y_arr = [dict(hist)[j] for j in dict(hist).keys()]

    x_arr_hist = []
    y_arr_hist = []

    while (len(x_arr) > 0):

        x_arr_hist.append(min(x_arr))
        y_arr_hist.append(y_arr[x_arr.index(min(x_arr))])
        holder = x_arr.index(min(x_arr))
        del x_arr[holder]
        del y_arr[holder]

    plt.plot(x_arr_hist, y_arr_hist)
    plt.scatter(x_arr_hist, y_arr_hist)
    plt.show()



def initialization(circuit, qubits, number_qubits):
    # I initialize the coin as |1> 
    circuit.append(cirq.X(qubits[-1]))

    # and the walker
    circuit.append(cirq.X(qubits[1]))


hist, result = quantum_walk(step, initialization, 10, 10, 100)
print(hist)
graph(hist)