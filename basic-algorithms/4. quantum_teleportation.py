import cirq as q
import random

def quantum_teleportation(psi):
    num_qubits = 2

    # Setup
    circuit = q.Circuit()
    qalice = q.NamedQubit("alice")
    qbob = q.NamedQubit("bob")
    qubits = [qalice, qbob]

    circuit.append(q.X(psi)**0.25)


    # H on the first qubit and CNOT(qalice, qbob)
    circuit.append(q.H(qalice))
    circuit.append(q.CNOT(qalice, qbob))

    # Apply CNOT(psi, alice)
    circuit.append(q.CNOT(psi, qalice))

    # Apply H(psi)
    circuit.append(q.H(psi))

    # Apply measurements
    m1 = q.Moment()
    m1 += q.measure(qalice, key='alice')
    m1 += q.measure(psi, key='psi')

    circuit.append(m1)

    # Read the value of qalice, if it returns |1>, apply X(qbob)
    circuit.append(q.CNOT(qalice, qbob))
    
    # Read the value of psi, if it returns |1>, apply Z(qbob)
    circuit.append(q.CZ(psi, qbob))

    return circuit

psi = q.NamedQubit("psi")

circ = quantum_teleportation(psi)
print(circ)

simulator = q.Simulator()
result = simulator.simulate(circ)
bobs_bloch_vector = q.bloch_vector_from_state_vector(result.final_state_vector, index=1)

print("Bloch vector of Bob's qubit:")
print(bobs_bloch_vector)
