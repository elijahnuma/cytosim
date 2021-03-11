#!/usr/bin/env python
#!/usr/bin/env python3
import sys
sys.path.append('/usr/local/usrapps/belmonte/bin')

import os 
import shutil
import numpy as np

from CytoSimPhysics import *
from CytoSimDataExtraction import *

job_list = ['0' + str(i) if i<10 else str(i) for i in range(9999)]
## Variables to Record
Contraction_Metrics=[]
R_Metrics=[]
Para_Metrics=[]
tdata=[]

opath='/gpfs_common/share03/belmonte/egnuma/job{}/save'.format(job_list[0])
os.chdir(opath)

## Change the report used by CytoSimDataExtraction.py
set_report('reportGIT')

## Run through each run folder
count=0
for folder in sorted(os.listdir(opath)):

    ## Parameters to record
    fibers=0    
    motors=0
    linkers=0
    length=0
    size=0
    unbind=5
    bind=5
    v0=0
    rigid=0
    dwell=0
    unforce=0
    bindcount=0
    timeoff=0

## move to folder
    if os.path.isdir(folder):
        os.chdir(opath+'/'+folder)
        count += 1 
        if count>=0:
            

## extract info about the run conditions    
            FileName='config.cym'
            if os.path.isfile(FileName):
                File=open(FileName,'r')
                
                for line in File:
                    words=line.split()
                    if words!=[] and words[0]=='new':
                        if words[-1]=='motor' or words[-1]=='myosin' or words[-1]=='minifilament':
                            motors=int(words[1])
                        elif words[-1]=='crosslinker':
                            linkers=int(words[1])
                        elif words[-1]=='filament':
                            fibers=int(words[1])
                    if words!=[] and words[0]=='geometry':
                        size=float(words[-2])
                    if words!=[] and words[0]=='length':
                        length=float(words[-1])
                    if words!=[] and words[0]=='binding':
                        bind=float(words[-2][:-1])
                    if words!=[] and words[0]=='unbinding' and bindcount==0:
                        unbind=float(words[-2][:-1])
                        unforce=float(words[-1])   
                        bindcount=1
                    if words!=[] and words[0]=='max_speed':
                        v0=float(words[-1])
                    if words!=[] and words[0]=='rigidity':
                        rigid=float(words[-1])
                    if words!=[] and words[0]=='hold_growing_end':
                        dwell=float(words[-1])
                parameters=[fibers,motors,linkers,size,length,bind,unbind,v0,rigid,dwell,unforce,timeoff]
                Para_Metrics.append(parameters)

    ## extract sim results, calculate cluster sizes, rates, lengths etc... 
     
                fiberdict=read_fiber_points(os.getcwd())

                times=sorted(fiberdict.keys())
                tdata.append(times)
            
                Rs,dRdtmax,dRdtavg,dRdtfirst,dRdtone=get_contraction_rate(fiberdict)

                dRdt=[]

                for ti,tf,Ri,Rf in zip(times,times[1:],Rs,Rs[1:]):
                        dRdt.append((Rf-Ri)/(tf-ti))

                Contraction_Metrics.append(dRdt)
                R_Metrics.append(Rs)


                File.close()            
                os.chdir(opath)

    os.chdir(opath)
               
## Create folder and save results as csv files 
os.chdir(opath)
os.mkdir('Data_Files')
os.chdir('Data_Files')
FileName='Cdata.csv'
np.savetxt(FileName,Contraction_Metrics,delimiter=',')
FileName='Rdata.csv'
np.savetxt(FileName,R_Metrics,delimiter=',')
FileName='tdata.csv'
np.savetxt(FileName,tdata,delimiter=',')
FileName='Pdata.csv'
np.savetxt(FileName,Para_Metrics,delimiter=',')
os.chdir(opath)
