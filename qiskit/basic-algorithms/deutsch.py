from qiskit import QuantumCircuit, Aer, transpile

qc = QuantumCircuit(2,1)

# initialize in a Bell state both the qubits, so that the register is |+->
qc.x(1)
qc.h(0)
qc.h(1)

qc.barrier()

# apply the objective function
def f(qc):
    qc.cnot(0,1)
    qc.x(0)

f(qc)

qc.barrier()

# H on the first qubit and measure the first qubit, if it's 0 with certainty
# the function is constant, otherwise it's balanced
qc.h(0)
qc.measure(0,0)

print(qc)

# run
simulator = Aer.get_backend('aer_simulator')
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)
