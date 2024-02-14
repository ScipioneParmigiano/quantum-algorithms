from qiskit import QuantumCircuit, Aer, transpile

qc = QuantumCircuit(2)

# initialize in a Bell state, and A and B share a qubit
qc.h(0)
qc.cx(0,1)

qc.barrier() 

#  A performs a transformation (H) on her qubit (i.e. the circuit is multiplied by H ⊗ I)
# H depends on the bits A wanna share
def H(qc, final_message):
    if final_message == "00":
        # I ⊗ I
        pass

    elif final_message == "01":
        # X ⊗ I
        qc.x(0)

    elif final_message == "10":
        # Z ⊗ I
        qc.z(0)

    elif final_message == "11":
        # ZX ⊗ I
        qc.x(0)
        qc.z(0)

# apply the correct gates based on the final message
final_message = "11"
H(qc, final_message)

qc.barrier()

# then A transfer her qubit to B, that measures both the qubits with respect to the Bell basis
qc.cx(0,1)
qc.h(0)
qc.measure_all()

print(qc)

# run
simulator = Aer.get_backend('aer_simulator')
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)
