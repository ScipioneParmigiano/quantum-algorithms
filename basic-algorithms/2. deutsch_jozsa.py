import cirq

def deutsch_jozsa(function, num_qubits):

    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(num_qubits)

    m0 = cirq.Moment(cirq.X(qubits[-1]))
    m1 = cirq.Moment()
    m2 = cirq.Moment()

    for qubit in qubits:
        m1 += cirq.H(qubit)

    circuit.append(m0)
    circuit.append(m1)

    function(circuit)

    for qubit in qubits:
        m2 += cirq.H(qubit)

    circuit.append(m2)
    circuit.append(cirq.measure(qubits[:-1]))

    s = cirq.Simulator()
    results = s.simulate(circuit)

    contains_one = any(1 in values for values in results.measurements.values())
    
    if contains_one:
        return True # balanced
    else: 
        return False # constant

def constant_function(circuit):
    pass

def balanced_function(circuit):
    qubits = list(circuit.all_qubits())

    circuit.append(cirq.CNOT(qubits[1], qubits[0]))
    circuit.append(cirq.Z(qubits[0]))


print(deutsch_jozsa(constant_function, 5))
print(deutsch_jozsa(balanced_function, 4))
