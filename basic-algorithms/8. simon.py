import cirq
import numpy as np
import scipy as sp
from collections import Counter

def simon(function, secret_string, nrep=50):
    data = []

    for _ in range(nrep):
        v = False
        while not v:
            #setup
            len_q = len(secret_string)

            qubits1 = cirq.LineQubit.range(len_q)
            qubits2 = cirq.LineQubit.range(len_q, 2*len_q)
            c = cirq.Circuit()

            # H on first register
            c.append(cirq.H.on_each(*qubits1))

            # query to the oracle
            function(c, qubits1, qubits2, secret_string)
            
            # H on first register
            c.append(cirq.H.on_each(*qubits1))

            # measure
            c.append(cirq.measure(qubits1, key="m"))

            # simulate
            sim = cirq.Simulator()
            run = sim.run(c)
            results = [sim.run(c).measurements["m"][0] for _ in range(len_q - 1)]

            v = processing(data, results)

    freqs = Counter(data)
    print(c)
    print(f"Secret string: {secret_string}")
    print(f"Answer: {freqs.most_common(1)[0][0]}")


def processing(data, results):
    sv = sp.linalg.svdvals(results)
    tol = 1e-5

    # check if measurements are linearly dependent
    if sum(sv < tol) == 0:  
        v = True

        null_space = sp.linalg.null_space(results).T[0]
        solution = np.around(null_space, 3) 
        minval = abs(min(solution[np.nonzero(solution)], key=abs))

        # renormalization vector mod 2
        solution = (solution / minval % 2).astype(int)  
        data.append(str(solution))

        return v


def u(circuit, q1, q2, secret_string):
    for i, j  in zip(q1, q2):
        circuit.append(cirq.CNOT(i, j))

    signif = next((i for i, bit in enumerate(secret_string) if bit), None)

    if signif is not None:
        for j, bit in enumerate(secret_string):
            if bit:
                circuit.append(cirq.CNOT(q1[signif], q2[j]))

    circuit.append(cirq.SWAP(q2[0], q2[-1]))


secret = np.random.randint(2, size=5)

simon(u, secret)