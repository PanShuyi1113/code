import matplotlib.pyplot as plt
import numpy as np
import scipy
from qutip import basis, sigmax, sigmaz
from qutip_qip.circuit import QubitCircuit
from qutip_qip.device import LinearSpinChain
import qutip_qip
from qutip.ipynbtools import version_table

pi = np.pi
num_samples = 500
amp = 0.1
f = 0.5
t2 = 10 / f

# Define a processor.
proc = LinearSpinChain(num_qubits=1, sx=amp / 2, t2=t2)
ham_idle = 2 * pi * sigmaz() / 2 * f
resonant_sx = 2 * pi * sigmax() - ham_idle / (amp / 2)
proc.add_drift(ham_idle, targets=0)
proc.add_control(resonant_sx, targets=0, label="sx0")


# Define a Ramsey experiment.
def ramsey(t, proc):
    qc = QubitCircuit(1)
    qc.add_gate("RX", 0, arg_value=pi / 2)
    qc.add_gate("IDLE", 0, arg_value=t)
    qc.add_gate("RX", 0, arg_value=pi / 2)
    proc.load_circuit(qc)
    result = proc.run_state(init_state=basis(2, 0), e_ops=sigmaz())
    return result.expect[0][-1]


idle_tlist = np.linspace(0.0, 30.0, num_samples)
measurements = np.asarray([ramsey(t, proc) for t in idle_tlist])

rx_gate_time = 1 / 4 / amp  # pi/2
total_time = 2 * rx_gate_time + idle_tlist[-1]
tlist = np.linspace(0.0, total_time, num_samples)

peak_ind = scipy.signal.find_peaks(measurements)[0]


def decay_func(t, t2, f0):
    return f0 * np.exp(-1.0 / t2 * t)


(t2_fit, f0_fit), _ = scipy.optimize.curve_fit(
    decay_func, idle_tlist[peak_ind], measurements[peak_ind]
)
print("T2:", t2)
print("Fitted T2:", t2_fit)

fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
ax.plot(idle_tlist[:], measurements[:], "-", label="Simulation",
        color="slategray")
ax.plot(
    idle_tlist,
    decay_func(idle_tlist, t2_fit, f0_fit),
    "--",
    label="Theory",
    color="slategray",
)
ax.set_xlabel(r"Idling time $t$ [$\mu$s]")
ax.set_ylabel("Ramsey signal", labelpad=2)
ax.set_ylim((ax.get_ylim()[0], ax.get_ylim()[1]))
ax.set_position([0.18, 0.2, 0.75, 0.75])
ax.grid()