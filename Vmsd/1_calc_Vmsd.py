import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Set global font size to 14
plt.rcParams.update({'font.size': 12})

input_dir = 'ta_msd_data_CoM'
prefix = "<prefix>"
# Targets in picoseconds (ps)
delta_targets = [1000.0, 10000.0, 30000.0, 40000.0, 60000.0, 100000.0] 
colors = ['red', 'orange', 'green', 'blue', 'purple', 'black']
labels = ['1 ns', '10 ns', '30 ns', '40 ns', '60 ns', '100 ns']

# Identify available T values (frames) and Replicas
files = glob.glob(os.path.join(input_dir, f"CoMmsd_{prefix}_r0*_T*.txt"))
T_values = sorted(list(set([int(f.split('_T')[1].split('.txt')[0]) for f in files])))
replica_indices = sorted(list(set([int(f.split('_r0')[1].split('_T')[0]) for f in files])))

# Sample dt from first file
sample_data = np.loadtxt(files[0])
dt = sample_data[1, 0] - sample_data[0, 0] 

eb_vs_T = {d: [] for d in delta_targets}
T_ps_axis = {d: [] for d in delta_targets}

for T in T_values:
    for delta_target in delta_targets:
        msds_at_delta = []
        for r in replica_indices:
            f_path = os.path.join(input_dir, f"CoMmsd_{prefix}_r0{r}_T{T}.txt")
            if os.path.exists(f_path):
                data = np.loadtxt(f_path)
                lags, msd_vals = data[:, 0], data[:, 1]
                if delta_target <= lags[-1]: 
                    idx = np.abs(lags - delta_target).argmin()
                    msds_at_delta.append(msd_vals[idx])
        
        if len(msds_at_delta) == len(replica_indices):
            eb = np.var(msds_at_delta) / (np.mean(msds_at_delta)**2)
            eb_vs_T[delta_target].append(eb)
            T_ps_axis[delta_target].append(T * dt)

plt.figure(figsize=(6, 4.5)) 

for i, delta in enumerate(delta_targets):
    if eb_vs_T[delta]:
        T_ns_axis = np.array(T_ps_axis[delta]) / 1000.0
        plt.plot(T_ns_axis, eb_vs_T[delta], 'o-', color=colors[i], label=rf'$\tau$ = {labels[i]}')

plt.xscale('log')
plt.xlabel('Observation Time, T [ns]')
plt.ylabel(rf'V$_{{{{MSD}}}}$($\tau$, T)')
plt.ylim(-0.005, 0.21)
plt.xlim(1, 12000)
plt.legend(fontsize=12, labelspacing=0.1, handletextpad=0.4, borderaxespad=0.3)

plt.tight_layout()
plt.savefig(f"Vmsd_{prefix}.png", dpi=300, bbox_inches="tight")
plt.close()
