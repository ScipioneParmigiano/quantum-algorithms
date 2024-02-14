from qiskit import QuantumCircuit, Aer, transpile

qc = QuantumCircuit(3,3) # |AB\psi>

# init bell state
qc.h(0)
qc.cx(1, 0)

qc.barrier() 

# prepare the qubit to be sent
def prep(qc):
    qc.h(2)

prep(qc)

qc.barrier() 


# cnot and H
qc.cx(2,0)
qc.h(2)

qc.barrier() 

# measure
qc.measure(0, 0)
qc.measure(2, 2)

qc.barrier()

# Bob processing
qc.x(1)
qc.z(1)

qc.barrier()

qc.measure(1, 1)

print(qc)

# run
simulator = Aer.get_backend('aer_simulator')
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)
