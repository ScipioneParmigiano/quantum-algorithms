import cirq as q
import random

def grover(function, num_qubits):

    # Setup
    circuit = q.Circuit()
    qubits = q.LineQubit.range(num_qubits)
    ancilla = q.LineQubit(num_qubits)

    m0 = q.Moment()
    for qubit in qubits:
        m0 += q.H(qubit)

    circuit.append(m0)

    circuit.append(q.X(ancilla))
    circuit.append(q.H(ancilla))

    # Oracle
    function(circuit, ancilla)

    # Grover operator
    m1 = q.Moment()
    m2 = q.Moment()

    for qubit in qubits:
        m1 += q.H(qubit)
        m2 += q.X(qubit)
    
    circuit.append(m1)
    circuit.append(m2)
    circuit.append(q.H(qubits[1]))
    circuit.append(q.CNOT(qubits[0], qubits[1]))
    circuit.append(q.H(qubits[1]))
    circuit.append(m2)
    circuit.append(m1)

    circuit.append(q.measure(qubits, key="result"))

    print(circuit)

    return(circuit)

def oracle(circuit, ancilla):
    qubits = list(circuit.all_qubits())

    for qubit, bit in zip(qubits, xprime):
        if not bit:
            circuit.append(q.X(qubit))

    circuit.append(q.TOFFOLI(qubits[0], qubits[1], ancilla))

    for qubit, bit in zip(qubits, xprime):
        if not bit:
            circuit.append(q.X(qubit))


def bitstring(bits):
    return "".join(str(int(b)) for b in bits)


nqubits = 2
xprime = [random.randint(0, 1) for _ in range(nqubits)]
print(f"Bitstring: {xprime}")

grover_circ = grover(oracle, nqubits)
simulator = q.Simulator()

result = simulator.run(grover_circ, repetitions=10)

frequencies = result.histogram(key="result", fold_func=bitstring)

most_common_bitstring = frequencies.most_common(1)[0][0]

print("Solution:\n{}".format(frequencies))
print("\nGrover's algorthithm solution: {}".format(most_common_bitstring))
