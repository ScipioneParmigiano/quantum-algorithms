from qiskit import QuantumCircuit, Aer, transpile

qc = QuantumCircuit(4,3)

# initialize in a Bell state all the qubits, so that the register is |+>^n |->
qc.x(3)

qc.h(0)
qc.h(1)
qc.h(2)
qc.h(3)

qc.barrier()

# apply the objective function
def f(qc):
    qc.cnot(0,3)
    qc.x(0)

f(qc)

qc.barrier()

# H on all the qubits but the last one and measure the first n-1 qubits, if there's no 1, with certainty
# the function is constant, otherwise it's balanced
qc.h(0)
qc.h(1)
qc.h(2)

qc.barrier()

qc.measure([0,1,2],[0,1,2])

print(qc)

# run
simulator = Aer.get_backend('aer_simulator')
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)
