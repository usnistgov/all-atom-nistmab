#!/bin/bash
#SBATCH -J <job>
#SBATCH -o ../slurm_outputs/output.slurm.out
#SBATCH --mem=64G
#SBATCH --cpus-per-task=16
#SBATCH --time=2-10:00:00
#
prefix="<prefix>"
#rep="r01"
topo="<prmtop>"
for rep in "r01" "r02" "r03" "r04";
do
#
cpptraj << EOF
parm <prmtop>_${rep}_noWat.prmtop
trajin <traj1>_${rep}.nc 1 last
trajin <traj2>_${rep}.nc 1 last
strip !(:1-1343)
unwrap bymol
trajout ../unwrapped_noions/<name>.nc
prnlev 3
go
EOF
#
cpptraj << EOF
parm <prmtop>.prmtop
parmstrip !(:1-1343)
parmwrite out ../unwrapped_noions/<prmtop>.prmtop
go
EOF
#
done
