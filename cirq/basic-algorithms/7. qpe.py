import cirq
import numpy as np

def qpe(oracle, num_qubits, preparation_gate = cirq.X):
    
    # Setup
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(num_qubits)
    psi = cirq.LineQubit(num_qubits)

    # X gate on psi so that we have non trivial phase
    circuit.append(preparation_gate(psi))

    # Hadamard gate on the first n-1 qubits
    h = cirq.H.on_each(qubits)
    circuit.append(h)

    # Apply the controlled oracle
    for i, bit in enumerate(qubits):
        circuit.append(cirq.ControlledGate(oracle).on(bit, psi) ** (2 ** (num_qubits - i - 1)))


    # Apply IQFT
    circuit.append(iqft(qubits[::-1]))
    

    # Measurements
    circuit.append(cirq.measure(qubits, key="measurement"))

    # print(circuit)
    return circuit
    

def iqft(qubits):
    qr = list(qubits)[::-1]
    operations = []

    while len(qr) > 0:
        q_head = qr.pop(0)

        # Hadamard
        operations.append(cirq.H(q_head))
        for i, qubit in enumerate(qr):

            # CZ
            cz_operation = cirq.CZ(qubit, q_head) ** (-1 / (2 ** (i + 1)))
            operations.append(cz_operation)
    
    return operations

theta = 0.5139861892
oracle = cirq.Z ** (2 * theta)
num_qubits = 10
pe = qpe(oracle, num_qubits, cirq.X)


# Simulation
s = cirq.Simulator()
result = s.run(pe, repetitions=5)

# Convert from bits to theta
powers_of_2 = 2 ** np.arange(num_qubits)
measurements = result.measurements["measurement"]

sum_along_rows = np.sum(powers_of_2 * measurements, axis=1)
theta_hat = sum_along_rows / 2**num_qubits

print(f"estimated values: {theta_hat}")
print(f"avg: {np.mean(theta_hat)}")

