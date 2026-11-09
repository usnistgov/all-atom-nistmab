#!/bin/bash
#SBATCH -J liquidlib_SUFFIX
#SBATCH -o slurm_SUFFIX.out
#SBATCH --mem=16GB
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=6:10:00
printf "_________\nBegin:\n"
conda activate ambertools
#

~/software/LiquidLib-develop-gpu/build/LiquidLib -flagfile=cisf_SUFFIX.in > cisf_calculation_SUFFIX.liquidlib.out
printf "\nLiquidLib calculation complete\n"
