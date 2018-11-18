# Thanks to http://kth.diva-portal.org/smash/get/diva2:1214481/FULLTEXT01.pdf for helping me undestand quantum computing better.
from cccZ import cccZ
import qiskit as qk

qr = qk.QuantumRegister(4)
cr = qk.ClassicalRegister(4)
qc = qk.QuantumCircuit(qr, cr)

# First we set all qubits to superposition
# All states have the amplitude of 1/sqrt(N), N = 16 because 4 qbits have 16 possibilities

# Hadamard Gate -> u2(+0, +pi) -> u3(+pi/2, +0, +pi)
qc.h(qr)

# The amplitude of each state at this point is 0.25
# We need to invert the amplitude of the state we look for

# bit-flip gate -> u3(+pi, +0, +pi)
qc.x(qr[0]) # u3(+pi, +0, +pi) to 0
qc.x(qr[2]) # u3(+pi, +0, +pi) to 2
qc.x(qr[3]) # u3(+pi, +0, +pi) to 3

cccZ(qc, qr[0], qr[1], qr[2], qr[3]) # Triple controlled Pauli Z-gate

# bit-flip gate -> u3(+pi, +0, +pi)
qc.x(qr[0]) # u3(+pi, +0, +pi) to 0
qc.x(qr[2]) # u3(+pi, +0, +pi) to 2
qc.x(qr[3]) # u3(+pi, +0, +pi) to 3

# At this point the amplitude of the state 0010 has been turned to -0.25
# Flip all amplitudes around the avarage so the amplitude of the state we look for increases

qc.h(qr) # u3(+pi/2, +0, +pi)
qc.x(qr) # u3(+pi, +0, +pi)

cccZ(qc, qr[0], qr[1], qr[2], qr[3]) # Triple controlled Pauli Z-gate

qc.x(qr)  # u3(+pi, +0, +pi)
qc.h(qr) # u3(+pi/2, +0, +pi)

# The avarage amplitude is (15*(0.25)-0.25)/16 = 0.21875
# The difference between the state 0010 and the avarage is 0.21875 - (-0.25) = 0.46875
# Inversion around the avarage gives the state 0010 the amplitude of 0.21875 + 0.46875 = 0.6875
# Using the same method for the other values the get the amplitude of 0.1875.

# A barrier is applied to prevent any optimization that could possibly reorder the gates
qc.barrier(qr)
qc.measure(qr, cr)

# loads the backend
qasm = qk.Aer.get_backend('qasm_simulator_py')

# simulate the circuit locally and get results
coupling_map = [[0, 1], [0, 2], [1, 2], [3, 2], [3, 4], [4, 2]]
qasm_job = qk.execute(qc, backend=qasm, shots=8192, coupling_map=coupling_map)
qasm_results = qasm_job.result()

qc_counts = qasm_results.get_counts(qc)

print(qc_counts)
