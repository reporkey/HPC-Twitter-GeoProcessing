#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --output="1node8task.out"

module load Python/3.5.2-goolf-2015a

time mpiexec python3 __main__.py
