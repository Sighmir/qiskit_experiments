import time
import qiskit as qk

qr = qk.QuantumRegister(2)
cr = qk.ClassicalRegister(2)
qc = qk.QuantumCircuit(qr, cr)

qc.h(qr[0])  # Hadamard Gate: puts the first qubit in superposition (equal probability for 0 and 1)
qc.cx(qr[0], qr[1])  # Controlled NOT: puts the first and the second qubit in a bell state (quantum entanglement)

mz = qk.QuantumCircuit(qr,cr)
mz.measure(qr, cr) # measure both qubits on Z basis (computational basis) and stores the results on the classical register

mx = qk.QuantumCircuit(qr, cr)
mx.h(qr)  # measures each qubit on the X basis (superposition basis) and stores the results on the classical register
mx.measure(qr, cr)

# entangling circuits
tz = qc + mz
tx = qc + mx

# load ibmq backend
qk.IBMQ.load_accounts()
ibmqxf = qk.IBMQ.get_backend('ibmqx4')

# executes the circuit remotelly and wait for it to be done
ibmqxf_job = qk.execute([tz, tx], backend=ibmqxf, shots=1024)

lapse = 0
interval = 10
job_status = ibmqxf_job.status()
while job_status.name != 'DONE':
  ibmqxf_status = ibmqxf.status()
  job_status = ibmqxf_job.status()
  print('Time elapsed: {} seconds'.format(interval * lapse))
  print('Job Status: {} - Pending Jobs: {} - Operational: {}'.format(job_status,ibmqxf_status['pending_jobs'],ibmqxf_status['operational']))
  time.sleep(interval)
  lapse += 1

# get results once execution has finished
ibmqxf_results = ibmqxf_job.result()

tz_counts = ibmqxf_results.get_counts(tz)
tx_counts = ibmqxf_results.get_counts(tx)

print(tz_counts)
print(tx_counts)
