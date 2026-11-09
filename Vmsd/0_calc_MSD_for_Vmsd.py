import numpy as np
import MDAnalysis as mda
from MDAnalysis.analysis import msd
import os
import matplotlib.pyplot as plt

prefix = "<prefix>"
trajectories = [f"<path>_{prefix}_r0{rep}_unwrapped.nc" for rep in range(1, 5)]
topology = f"<path>_{prefix}_r01_unwrapped.prmtop"

# Selection for Center of Mass
selection = 'resid 1:1343' 
output_dir = 'ta_msd_data_CoM'
plot_dir = 'individual_msd_plots_CoM'

for d in [output_dir, plot_dir]:
    if not os.path.exists(d):
        os.makedirs(d)

T_frames = np.unique(np.logspace(np.log10(2), np.log10(20000), num=60, dtype=int))

def generate_aged_msds(topo, traj, rep_idx):
    u = mda.Universe(topo, traj, format="NC")
    dt = u.trajectory.dt
    protein = u.select_atoms(selection)
    
    for T in T_frames:
        out_name = os.path.join(output_dir, f'CoMmsd_{prefix}_r0{rep_idx}_T{T}.txt')
        
        # Calculate CoM trajectory for the slice [0:T]
        # mass_traj shape: (n_frames, n_atoms, 3)
        com_coords = np.array([protein.center_of_mass() for ts in u.trajectory[:T]])[:, np.newaxis, :]
        
        # Create virtual universe for CoM point
        v_univ = mda.Universe.empty(n_atoms=1, n_residues=1, atom_resindex=[0], trajectory=True)
        v_univ.load_new(com_coords)
        
        # Run MSD on the virtual CoM atom
        msd_analyzer = msd.EinsteinMSD(v_univ.atoms, msd_type='xyz', fft=True)
        msd_analyzer.run()
        
        msd_values = msd_analyzer.results.timeseries
        lags_ps = np.arange(len(msd_values)) * dt
        
        # Save data
        data = np.column_stack((lags_ps, msd_values))
        np.savetxt(out_name, data, header=f'lag_time_ps CoM_msd_angstrom2 (T={T} frames)')

if __name__ == "__main__":
    for i, traj in enumerate(trajectories):
        print(f"Processing replica {i+1}...")
        generate_aged_msds(topology, traj, i+1)
