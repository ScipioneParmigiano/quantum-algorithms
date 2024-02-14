import cirq

def qft(qubits):
    qr = list(qubits)
    operations = []

    for idx, q_head in enumerate(qr):
        # Hamard
        operations.append(cirq.H(q_head))

        for i, qubit in enumerate(qr[idx+1:], start=1):
            
            # CZ
            cz = cirq.CZ(qubit, q_head) ** (1 / (2 ** (i + 1)))
            operations.append(cz)

    return operations


q = cirq.LineQubit.range(3)
result = cirq.Circuit(qft(q))
print(result)

