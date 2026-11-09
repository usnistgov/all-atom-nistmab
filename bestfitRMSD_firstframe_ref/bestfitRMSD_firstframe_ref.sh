#!/bin/bash
#SBATCH -J <name>
#SBATCH -o ../slurm_outputs/output.slurm.out
#SBATCH --mem=64G
#SBATCH --cpus-per-task=16
#SBATCH --time=1-10:00:00
conda activate ambertools
###
#rep="r01"
sim="<prefix>"
for rep in "r01" "r02" "r03" "r04";
do
cpptraj << EOF
parm ../unwrapped/<file>_${rep}_unwrapped.prmtop
trajin ../unwrapped/<file>_${rep}_unwrapped.nc 1 20000
rmsd fab1 (:1-213|:214-430)&(@CA) first out rmsd_fab1_${sim}_${rep}_Calpha_first.dat nomod
rmsd fab2 (:1114-1326|:664-880)&(@CA) first out rmsd_fab2_${sim}_${rep}_Calpha_first.dat nomod
rmsd fc (:455-663|:905-1113|:1327-1335|:1336-1343)&(@CA) first out rmsd_fc_${sim}_${rep}_Calpha_first.dat nomod

rms allTR (:1-1343)&(@CA) first out rmsd_all_${sim}_${rep}_Calpha_first.dat
run
EOF
done
###
