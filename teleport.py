import qiskit as qk

qr = qk.QuantumRegister(3)
cr0 = qk.ClassicalRegister(1)
cr1 = qk.ClassicalRegister(1)
cr2 = qk.ClassicalRegister(1)
qc = qk.QuantumCircuit(qr, cr0, cr1, cr2)

# Prepare an initial state
qc.u3(0.3, 0.2, 0.1, qr[0])  # U3 gate: sets the angle of x,y,z in radians ?

# Prepare a Bell pair
qc.h(qr[1])
qc.cx(qr[1], qr[2])

# Barrier following state preparation
qc.barrier(qr)

# Measure in the Bell basis
qc.cx(qr[0], qr[1])
qc.h(qr[0])
qc.measure(qr[0], cr0[0])
qc.measure(qr[1], cr1[0])

# Apply a correction
qc.z(qr[2]).c_if(cr0, 1) # phase-flip(+0, +0, +pi)
qc.x(qr[2]).c_if(cr1, 1) # Classical NOT gate (+pi, +0, +pi) bit-flip
qc.measure(qr[2], cr2[0])

# loads the backend
qasm = qk.Aer.get_backend('qasm_simulator_py')

# simulate the circuit locally and get results
coupling_map = [[0, 1], [0, 2], [1, 2], [3, 2], [3, 4], [4, 2]]
qasm_job = qk.execute(qc, backend=qasm, shots=1024, coupling_map=coupling_map)
qasm_results = qasm_job.result()

qc_counts = qasm_results.get_counts(qc)

print(qc_counts)
