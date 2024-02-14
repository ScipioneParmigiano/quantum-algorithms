from qiskit import QuantumCircuit, Aer, transpile

s = "111"
n = len(s)
qc = QuantumCircuit(n*2, n)

# initialize as \frac{1}{\sqrt{2^n}} \sum |X>|0> where X is a n-1 qubit
# register
qc.h(range(n))

qc.barrier()

# apply the query function, and get \frac{1}{\sqrt{2^n}} \sum |X>|f(X)>
def f(qc, s):
    s = s[::-1] # reverse s for easy iteration
    for i in range(n):
        qc.cx(i, i+n)
    if "1" not in s: 
        return qc  # 1:1 mapping, exits
    i = s.find("1") # index of first non-zero bit in s

    for j in range(n):
        if s[j] == "1":
            qc.cx(i, (j)+n)
    return qc

f(qc, s)

qc.barrier()

# apply H on all the first n-1 qubits (i.e. on X)
qc.h(range(n))

# measure X
qc.measure([i for i in range(0, n)], [i for i in range(0, n)]) 

print(qc)

# run
simulator = Aer.get_backend("aer_simulator")
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)

# at this point, the value of s is found by solving the omogeneous sistem As=0 where A are the measured value of the X register.abs
# This can be solved classically in polynomial time  