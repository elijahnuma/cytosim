#!/bin/tcsh
#BSUB -n 1
#BSUB -W 720
#BSUB -M 150000
#BSUB -J mycode
#BSUB -o stdout.%J
#BSUB -e stderr.%J
#BSUB -R select[avx]
bash sub
