#!/bin/tcsh
#BSUB -n 1
#BSUB -q belmonte
#BSUB -W 720
#BSUB -M 16GB
#BSUB -J mycode
#BSUB -o stdout.%J
#BSUB -e stderr.%J
#BSUB -R select[avx]
CheckReRun.py f mem=32GB ../../../job100
