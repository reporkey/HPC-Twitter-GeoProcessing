#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output="1node1task.out"

module load Python/3.5.2-goolf-2015a

time mpiexec python3 __main__.py
