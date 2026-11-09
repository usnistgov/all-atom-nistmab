#!/bin/bash
#SBATCH -J cluster4kmeans
#SBATCH -o cluster_4kmeans.slurm.out
#SBATCH --mem=64G
#SBATCH --cpus-per-task=32
#SBATCH --time=6-10:00:00

conda activate ambertools
###
sim="<prefix>"
r01first=52588
r02first=52565
r03first=52582
r04first=52557

GLOBAL_START=15001
GLOBAL_STOP=115000
OFFSET=10

r01lastread=$(( GLOBAL_START + ((r01first - GLOBAL_START) / OFFSET) * OFFSET ))
r02lastread=$(( GLOBAL_START + ((r02first - GLOBAL_START) / OFFSET) * OFFSET ))
r03lastread=$(( GLOBAL_START + ((r03first - GLOBAL_START) / OFFSET) * OFFSET ))
r04lastread=$(( GLOBAL_START + ((r04first - GLOBAL_START) / OFFSET) * OFFSET ))

r01start=$(( (r01lastread + OFFSET) - r01first ))
r02start=$(( (r02lastread + OFFSET) - r02first ))
r03start=$(( (r03lastread + OFFSET) - r03first ))
r04start=$(( (r04lastread + OFFSET) - r04first ))

r01stop=$((GLOBAL_STOP - r01first))
r02stop=$((GLOBAL_STOP - r02first))
r03stop=$((GLOBAL_STOP - r03first))
r04stop=$((GLOBAL_STOP - r04first))

#####
numclusters=4
cpptraj << EOF
parm <path>/<parm>.prmtop
trajin <path>/<traj1>_r01.nc 15000 last 10
trajin <path>/<traj2>_r01.nc $r01start $r01stop 10
trajin <path>/<traj1>_r02.nc 15000 last 10
trajin <path>/<traj2>_r02.nc $r02start $r02stop 10
trajin <path>/<traj1>_r03.nc 15000 last 10
trajin <path>/<traj2>_r03.nc $r03start $r03stop 10
trajin <path>/<traj1>_r04.nc 15000 last 10
trajin <path>/<traj2>_r04.nc $r04start $r04stop 10
rms first (:1-1343)
cluster ${sim}data_${numclusters}kmeans rms @CA kmeans clusters ${numclusters} savepairdist pairdist pairdist_${sim}_${numclusters}kmeans summary summary_${sim}_${numclusters}kmeans.dat info info_${sim}_${numclusters}kmeans.dat splitframe 10000,20000,30000 summarysplit split_summary_${sim}_${numclusters}kmeans.dat singlerepout comb_${sim}_${numclusters}kmeans.nc singlerepfmt netcdf out clustermembership_${sim}_${numclusters}kmeans.dat
run
EOF
done

