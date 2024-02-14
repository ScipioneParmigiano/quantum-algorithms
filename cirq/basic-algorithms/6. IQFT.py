import cirq 

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


q = cirq.LineQubit.range(3)
result = cirq.Circuit(iqft(q))
print(result)

