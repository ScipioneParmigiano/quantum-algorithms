from qiskit import QuantumCircuit, Aer, transpile
from math import pi as pi
from numpy import ceil as ceil

# let U_f be a black box s.t. f:{0,1}^n --> {0,1}
def u_f(qc):
    qc.cz(0, 2)
    qc.cz(1, 2)

# We want to find an input x \isin {0,1}^n s.t. f(x)=1
n = 3

qc = QuantumCircuit(n,n)

# apply H to the |00..0> register to get the state \frac{1}{\sqrt{2^n}}\sum_{x=0}^{N-1}|x>
qc.h(range(n))

# build the grover iterator (G from now on), i.e. the H U_s H U_f where U_s is an n-qubit phase shift operator
def grover_iterator(qc):
    u_f(qc)
    qc.h(range(n))
    # qc.z(range(n))
    qc.x(range(n))

    qc.h(n-1)
    qc.mct(list(range(n-1)), n-1)  # multi-controlled z-gate
    qc.h(n-1)

    qc.x(range(n))
    qc.h(range(n))

# apply G \frac{\pi}{4 \sqrt(n)} times
n_iter = pi/(4 * n**0.5)

print(ceil(n_iter))

for i in range(int(ceil(n_iter))):
    grover_iterator(qc)


# measure the output
qc.measure(range(n), range(n))

print(qc)

# run
simulator = Aer.get_backend('aer_simulator')
circ = transpile(qc, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)