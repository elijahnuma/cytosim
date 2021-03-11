#!/bin/tcsh
#BSUB -n 1
#BSUB -W 720
#BSUB -M 150000
#BSUB -J mycode
#BSUB -o stdout.%J
#BSUB -e stderr.%J
#BSUB -R select[avx]
bash analyzejobs.sh 90 110 114 rod
bash analyzejobs.sh 91 115 119 rod


