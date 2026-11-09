#!/bin/bash
#SBATCH -J unwrap
#SBATCH -o ../slurmoutputs/unwrap.out
#SBATCH --mem=16GB
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:1
#SBATCH --time=2-00:00:00
hostname
printf "_________\nBegin:\n"
conda activate ambertools
#
directoryname="<prefix>"
mkdir ${directoryname}
cd ${directoryname}

for replicate in "r01" "r02" "r03" "r04"
do
	fileprefix="${directoryname}_cisf_${replicate}"
	#
	printf "\nStarting computation for ${replicate}\n"
	#CONVERT TRAJECTORY TO XTC and GRO#
	cp ../amb_to_xtc.py amb_to_xtc_${replicate}.py
	sed -i -e "s/REP/${replicate}/g" amb_to_xtc_${replicate}.py
	sed -i -e "s/DIREC/${directoryname}/g" amb_to_xtc_${replicate}.py
	sed -i -e "s/PREFIX/${fileprefix}/g" amb_to_xtc_${replicate}.py
	#
	python amb_to_xtc_${replicate}.py > convert_${replicate}.out
	printf "\nTrajectory conversion complete\n"
done
###############################################################
printf "\nEND\n_________\n"
