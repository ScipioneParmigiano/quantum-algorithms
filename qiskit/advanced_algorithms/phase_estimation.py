from qiskit import QuantumCircuit, Aer, transpile
from math import pi as pi

# let  \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n-1} e^{2 \pi i \omega} |Y> where \omega \isin R and Y is the bynary encoding of the integer y 
# we want to estimate \omega (and \omega \isin (0,1) without loss of generality)

n = 12 # precision
qc = QuantumCircuit(n, n-1)

# initia
# lization: X on the 4th qubit
qc.x(n-1)

# H on the counting qubits
qc.h(range(n-1))

# change the phase using controlled phase gate
rep = 1
theta = 2*pi/3
for q in range(n-1):
    for i in range(rep):
        qc.cp(theta, q, n-1)
    rep *= 2

qc.barrier()

# apply the inverse of QFT
def IQFT(n, qc):
    for j in range(n//2): # swap
        qc.swap(j, n-j-1)
    for q in range(n): # H and control qubit
        for i in range(q): # controlled qubit
            qc.cp(-pi/(2**(q-i)), q, i) 
        qc.h(q)

IQFT(n-1, qc)

qc.barrier()

# measurements
qc.measure(range(n-1), range(n-1))

print(qc)

# run
simulator = Aer.get_backend("aer_simulator")
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
# print(counts)

# at this point to get the \omega we need to compute the decimal counterpart of the result and divide it by 2^n
most_freq_bits = [key for key, value in counts.items() if value > max(counts.values()) / 2]
ext_omega = int(most_freq_bits[0], 2)/(2**(n-1))
print(ext_omega)