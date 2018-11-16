import qiskit as qk

qr = qk.QuantumRegister(2)
cr = qk.ClassicalRegister(2)
qc = qk.QuantumCircuit(qr,cr)

qc.h(qr[0])  # Hadamard Gate: puts the first qubit in superposition (equal probability for 0 and 1)
qc.cx(qr[0], qr[1])  # Controlled NOT: puts the first and the second qubit in a bell state (quantum entanglement)

mz = qk.QuantumCircuit(qr,cr)
mz.measure(qr, cr) # measure both qubits on Z basis (computational basis) and stores the results on the classical register

mx = qk.QuantumCircuit(qr, cr)
mx.h(qr)
mx.measure(qr, cr) # measures each qubit on the X basis (superposition basis) and stores the results on the classical register

# entangling circuits
tz = qc + mz
tx = qc + mx

# loads the backend
qasm = qk.Aer.get_backend('qasm_simulator_py')

# simulate the circuit locally and get results
qasm_job = qk.execute([tz, tx], backend=qasm, shots=1024)
qasm_results = qasm_job.result()

tz_counts = qasm_results.get_counts(tz)
tx_counts = qasm_results.get_counts(tx)

print(tz_counts)
print(tx_counts)
