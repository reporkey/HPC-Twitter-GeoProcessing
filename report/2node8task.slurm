#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --output="2node8task.out"

module load Python/3.5.2-goolf-2015a

time mpiexec python3 __main__.py
