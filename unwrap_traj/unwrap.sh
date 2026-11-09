#!/bin/bash
#SBATCH -J job
#SBATCH -o ../slurm_outputs/output.slurm.out
#SBATCH --mem=64G
#SBATCH --cpus-per-task=16
#SBATCH --time=2-10:00:00
conda activate ambertools
#
prefix="<prefix>"
topo="<prmtop name>"
for rep in "r01" "r02" "r03" "r04";
do
#
cpptraj << EOF
parm <prmtop name>_${rep}.prmtop
trajin <traj1 path>_${rep}.nc 1 last 5
trajin <traj2 path>_${rep}.nc 1 last 5
unwrap bymol
trajout ../unwrapped/<name>.nc start 3001 stop 23000
prnlev 3
go
EOF
#
cpptraj << EOF
parm <prmtop name>.prmtop
parmstrip :WAT
parmwrite out ../unwrapped/<name>.prmtop
go
EOF
#
done
