#!/bin/sh
# ISF fitting script (0-40ns)
conda activate ambertools

directoryname="<prefix>_<suffix>"
cd ${directoryname}

# --- CONFIGURATION ---
windowSize=200
windowStride=5
lastwindow=$(echo 10000-${windowSize} | bc)

# Fit Range: 0 to 40 ns (0.040 microseconds)
FIT_START=0.000
FIT_END=0.040

for portion in "all" 
do
    replicate=2
    suffix="r0${replicate}_${portion}_s0_e${windowSize}"
    prefix="cisf_${suffix}"

    cat > fit_${directoryname}_${portion}.py <<EOF
import matplotlib.pyplot as plt
import numpy as np

# 1. Load Q-values and drop the first 3
zs = np.loadtxt('${prefix}_k')[3:] 
numZs = zs.shape[0]

# Setup window averaging
windowStride_avg = ${windowStride}
lastwindow_avg = ${lastwindow}
numFiles = len(range(0, lastwindow_avg + 1, windowStride_avg))

print(f"Processing ${portion}: Averaging {numFiles} windows for 0-40ns fit...")

zdataIndividual = []
t = None

for starttime in range(0, lastwindow_avg + 1, windowStride_avg):
    filename = f"cisf_r0${replicate}_${portion}_s{starttime}_e{starttime+${windowSize}}_coords"
    data = np.loadtxt(filename)
    if t is None: t = data[:, 0]
    zdataIndividual.append(data[:, 1:])

# Average windows: Shape (TimePoints, Q-values)
zdata = np.mean(np.array(zdataIndividual), axis=0)

# 2. Normalize and slice columns to drop the first 3
normZdata = (zdata / zdata[0, :])[:, 3:]

# --- PLOTTING & FITTING ---
fig, ax1 = plt.subplots(figsize=(5.4, 4.8))
cmap = plt.get_cmap('nipy_spectral')

all_deff, all_err = [], []

for i in range(numZs):
    color = cmap(i / numZs)
    z_iqt = normZdata[:, i]
    
    pmask = z_iqt > 0
    t_v = t[pmask]
    z_v = z_iqt[pmask]  # Raw values for plotting on log scale
    log_z = np.log(z_v) # Log values for linear regression

    # --- Linear Regression (y = mx) in log space ---
    mask = (t_v >= ${FIT_START}) & (t_v <= ${FIT_END})
    t_f, y_f = t_v[mask], log_z[mask]
    
    if len(t_f) > 1:
        denom = np.sum(t_f**2)
        slope = np.sum(t_f * y_f) / denom
        
        # Error calculation
        res = y_f - (slope * t_f)
        s2 = np.sum(res**2) / (len(t_f) - 1)
        std_err = np.sqrt(s2 / denom)
        
        all_deff.append(-slope / (zs[i]**2))
        all_err.append(std_err / (zs[i]**2))

        # --- PLOT DECAYS ---
        # Points: Larger (markersize=2.0) and darker (alpha=0.7)
        # Plotting z_v directly on a log scale
        plot_mask = t_v <= ${FIT_END}*3
        ax1.plot(t_v[plot_mask], z_v[plot_mask], 
                 'o', markersize=1.2, color=color, alpha=1.0, zorder=2)
        
        # Line: Solid ('-') and behind points (zorder=1)
        # Using exponential of the fit for log-scale straight lines
        t_plot = np.linspace(0, ${FIT_END}, 10)
        ax1.plot(t_plot, np.exp(slope * t_plot), '-', color=color, alpha=0.7, linewidth=1.5, zorder=1, label=f"{zs[i]:.2f} nm\$^{{-1}}\$")

# Enable Log Scale on Y-axis
ax1.set_yscale('log')

ax1.legend(loc='lower right', handlelength=0.8, labelspacing=0.1, handletextpad=0.5, fontsize=12, ncol=1)

ax1.set_xlabel('t [\$\mu\$s]', fontsize=14)
ax1.set_ylabel('I(Q,t) / I(Q,0)', fontsize=14)
ax1.set_ylim(0.2, 1.02) # Adjusted limits for log scale
ax1.set_xlim(0, 0.1)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tight_layout()
plt.savefig("decay_${portion}_${directoryname}_${replicate}.png", dpi=500)

# --- FINAL Deff PLOT ---
plt.figure(figsize=(8, 6))
plt.errorbar(zs, all_deff, yerr=all_err, fmt='o-', color='black', ecolor='red', capsize=3)
plt.xlabel('Q [nm\$^{-1}\$]', fontsize=14)
plt.ylabel('Deff [nm\$^2\$/\$\mu\$s]', fontsize=14)
plt.tight_layout()
plt.savefig("deff_${portion}_${directoryname}_${replicate}.png", dpi=500)
EOF
    python fit_${directoryname}_${portion}.py
done
