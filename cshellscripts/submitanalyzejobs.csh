#!/bin/tcsh
#BSUB -n 1
#BSUB -W 720
#BSUB -M 10GB
#BSUB -J mycode
#BSUB -o stdout.%J
#BSUB -e stderr.%J
#BSUB -R select[avx]
bash analyzejobs.sh 213 195 199 rod



