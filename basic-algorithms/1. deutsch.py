import cirq

def deutsch(function):
    circuit = cirq.Circuit()
    q0, q1 = cirq.LineQubit.range(2)

    m0 = cirq.Moment(cirq.X(q1))
    m1 = cirq.Moment(cirq.H(q0), cirq.H(q1))

    circuit.append(m0)
    circuit.append(m1)
    function(circuit)

    circuit.append(cirq.H(q0))
    circuit.append(cirq.measure(q0))

    s = cirq.Simulator()
    results = s.simulate(circuit)

    if results.measurements[str(q0)] == 1:
        return True # i.e. |1> balanced
    else: 
        return False # i.e. |0> constant


def constant_function(circuit):
    pass

def balanced_function(circuit):
    q0, q1 = circuit.all_qubits()

    circuit.append(cirq.CNOT(q1, q0))
    circuit.append(cirq.Z(q0))


print(deutsch(constant_function))
print(deutsch(balanced_function))
