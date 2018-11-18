import qiskit as qk
import math

qr = qk.QuantumRegister(1)
cr = qk.ClassicalRegister(1)

ux = qk.QuantumCircuit(qr, cr)
ux.u3(math.pi/2, 0, 0, qr[0]) # U3 gate: sets the angle of x,y,z in radians ? X = probability of 1 and 0 ? pi/2 == superposition ?
ux.x(qr[0]) # Classical NOT gate (+pi, +0, +pi) bit-flip
ux.measure(qr, cr)

uy = qk.QuantumCircuit(qr, cr)
uy.u3(0, math.pi, 0, qr[0]) # U3 gate: sets the angle of x,y,z in radians ? Y = ???
uy.y(qr[0])  # bit- and phase-flip (+pi, +pi/2, +pi/2)
uy.measure(qr, cr)

uz = qk.QuantumCircuit(qr, cr)
uz.u3(0, 0, math.pi, qr[0]) # U3 gate: sets the angle of x,y,z in radians ?
uz.z(qr[0]) # phase-flip (+0, +0, +pi)
uz.measure(qr, cr)

# loads the backend
qasm = qk.Aer.get_backend('qasm_simulator_py')

# simulate the circuit locally and get results
qasm_job = qk.execute([ux, uy, uz], backend=qasm, shots=1024)
qasm_results = qasm_job.result()

ux_counts = qasm_results.get_counts(ux)
uy_counts = qasm_results.get_counts(uy)
uz_counts = qasm_results.get_counts(uz)

print(ux_counts)
print(uy_counts)
print(uz_counts)
