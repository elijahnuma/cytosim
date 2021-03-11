from math import *
import numpy as np
import os, sys
from CytoSimDataExtraction import *

def get_cm(DICT):
    #DICT should be points dictionary for 1 time frame
    n = len(DICT)
    x=y=0
    if not n: return 0
    for id in DICT:
        m = len(DICT[id])
        for a,b in DICT[id]:    
            x += a
            y += b
    x = x/(n*m)
    y = y/(n*m)
    
    return [x,y]

def on_end(DICT):
    onend=[]
    for t in sorted(DICT):
        count=0
        for id in DICT[t]:
            if DICT[t][id][2]!='nan':
		if float(DICT[t][id][2])>=.9:
                	count += 1
        onend.append(count)
    return onend

def get_endtoend(DICT):
    EtE=[]
    for t in sorted(DICT):
        n = len(DICT[t])
        if not n: return 0
        EEtot=0
        for id in DICT[t]:
            EEtot += DICT[t][id]
        EtE.append(EEtot/n)
    return EtE

def get_mean_distance(DICT):

    R=[]
    for t in sorted(DICT):
        n = len(DICT[t])
        if not n: return 0
        x=y=xx=yy=0
        for id in DICT[t]:
            m = len(DICT[t][id])
            for a,b in DICT[t][id]:
                x += a
                y += b
                xx += a*a
                yy += b*b
      
        x = x/(n*m); xx = xx/(n*m)
        y = y/(n*m); yy = yy/(n*m)

        R.append(sqrt(2*(xx+yy-x*x-y*y)))
    
    return R

def get_contraction_rate(DICT):

    times = sorted(DICT.keys())
    R=get_mean_distance(DICT)
    dRdtmax=0
    dRdtsum=0
    dRdtfirst=0
    dRdtone=0
    count=0.0
    onesecond=0
    
    for ti,tf,Ri,Rf in zip(times,times[1:],R,R[1:]):
        dRdt=(Rf-Ri)/(tf-ti)
        dRdtsum += dRdt
        if dRdtfirst == 0:
            dRdtfirst += dRdt

        if abs(dRdt)>abs(dRdtmax):
            dRdtmax=dRdt

        if (tf-times[0])>=1.0 and onesecond==0:
            dRdtone=(Rf-R[0])/(tf-times[0])
            onesecond=1

        count += 1

    dRdtavg=dRdtsum/count

    return R,dRdtmax, dRdtavg, dRdtfirst, dRdtone

def get_motor_speed(CoupleDict,length):

    print 'Finding Motor Speeds'
    names= sorted(CoupleDict.keys())
    name=names[1]

    times = sorted(CoupleDict[name].keys())  
    t0=times[0]
    CIDS = sorted(CoupleDict[name][t0].keys())
 
    avgspeed=[]
    
    for ti,tf in zip(times,times[1:]):
        speed=0.0
        count=0.0        
        for id in CIDS:
            if CoupleDict[name][ti][id][2]!=0 and CoupleDict[name][ti][id][4]!=0 and CoupleDict[name][tf][id][2]!=0 and CoupleDict[name][tf][id][4]!=0:
                if CoupleDict[name][ti][id][3]!=length: 
                    head1i=CoupleDict[name][ti][id][3]
                    head1f=CoupleDict[name][tf][id][3]
                    v1=(head1f-head1i)/.2
                    speed+=v1
                    count+=1
                    
                if CoupleDict[name][ti][id][5]!=length:
                    head2i=CoupleDict[name][ti][id][5]
                    head2f=CoupleDict[name][tf][id][5]
                    v2=(head2f-head2i)/.2
                    speed+=v2
                    count+=1
        if count==0:
            avgspeed.append(speed)
        else:
            avgspeed.append(speed/count)

    return avgspeed
                            
                    


def get_bound_fibers(FiberDict,CoupleDict):

    print 'Finding Bound Fibers'

    times = sorted(FiberDict.keys())

    t0=times[0]
    CIDS = sorted(CoupleDict['motor'][t0].keys())

    boundfiber=[]
    
    for id in CIDS:
        if CoupleDict['motor'][t0][id][2]!=0 and CoupleDict['motor'][t0][id][4]!=0:
            if (not CoupleDict['motor'][t0][id][2] in boundfiber): boundfiber.append(CoupleDict['motor'][t0][id][2])
            if (not CoupleDict['motor'][t0][id][4] in boundfiber): boundfiber.append(CoupleDict['motor'][t0][id][4])

    BoundDict={}
    for t in times:
        BoundDict[t]={}
        for id in FiberDict[t]:
            if id in boundfiber:BoundDict[t][id]=FiberDict[t][id]

    return BoundDict

def get_bound_motors(CoupleDict,length):

    print 'Finding Bound Motors'

    times = sorted(CoupleDict['motor'].keys())

    t0=times[0]
    CIDS = sorted(CoupleDict['motor'][t0].keys())

    bound1=[]
    bound2=[]
    bound3=[]

    for t in times:
        count1=0
        count2=0
        count3=0
        for id in CIDS:
            if CoupleDict['motor'][t][id][2]!=0 and CoupleDict['motor'][t][id][4]!=0: 
                count1 += 1
                if CoupleDict['motor'][t][id][3]==length and CoupleDict['motor'][t][id][5]!=length: count2 += 1
                if CoupleDict['motor'][t][id][3]!=length and CoupleDict['motor'][t][id][5]==length: count2 += 1
                if CoupleDict['motor'][t][id][3]==length and CoupleDict['motor'][t][id][5]==length: count3 += 1

        bound1.append(count1)
        bound2.append(count2)
        bound3.append(count3)
                
    return bound1, bound2, bound3


def get_global_order_rate(DICT):

    times = sorted(DICT.keys())
    N=get_global_order(DICT)
    dNdtsum=0.0
    count=0.0
    for ti,tf,Ni,Nf in zip(times,times[1:],N,N[1:]):
        dNdtsum += (Nf-Ni)/(tf-ti)
        count += 1
    
    dNdtavg=dNdtsum/count
    return N,dNdtavg

def get_local_order_rate(DICT):

    times = sorted(DICT.keys())
    N=get_local_order(DICT)
    dNdtsum=0.0
    count=0.0
    for ti,tf,Ni,Nf in zip(times,times[1:],N,N[1:]):
        dNdtsum += (Nf-Ni)/(tf-ti)
        count += 1
    
    dNdtavg=dNdtsum/count
    return N,dNdtavg            

def get_orientation(DICT):

    print "Calculating Orientations"
  
    times = sorted(DICT.keys())
    Theta_Dict={}   
    
    xi=yi=xf=yf=d=dy=theta=0.0
    for t in times:
        Theta_Dict[t]=[]
        for id in DICT[t]:
        
            xi,yi=DICT[t][id][0]
            xf,yf=DICT[t][id][1]
            dx=xf-xi
            dy=yf-yi
            if dx==0 and dy>0:
                theta=pi/2
            elif dx==0 and dy<0:
                theta=3*pi/2
            else:
                theta=np.arctan(dy/dx)

            if dx<0:
                theta=theta+pi
            if theta<0:
                theta=theta+2*pi
            Theta_Dict[t].append(theta)
    
    return Theta_Dict     


def get_global_order(FiberData):
    """calculates global nematic order of fibers"""
    
    print "calculating global fiber segment alignment |", os.getcwd()
    
    NematicOrder = []   # Nematic order : NematicOrder[t] = metric
    
    for t in sorted(FiberData):
        Nfiber=len(FiberData[t])
        #auxiliary variables to calculate nematic order parameter
        c2=0; s2=0
        
        for id in FiberData[t]:
            Nsegment=len(FiberData[t][id])-1
            
            dx = FiberData[t][id][0][0] - FiberData[t][id][1][0]
            dy = FiberData[t][id][0][1] - FiberData[t][id][1][1]
            segment_length = sqrt(dx*dx+dy*dy)
            
            for A,B in zip(FiberData[t][id],FiberData[t][id][1:]):
                dx = B[0]-A[0]
                dy = B[1]-A[1]
                c = dx/segment_length  # cos()
                s = dy/segment_length  # sin()
        
                c2 += (1-2*s*s)  # c2 += cos(2a) = 1-2sin**2
                s2 += 2*c*s      # s2 += sin(2a) = 2*cos*sin
        
        NematicOrder.append(sqrt(c2**2 + s2**2)/(Nfiber*Nsegment))
    
    return NematicOrder

def get_local_order(FiberData):
    """calculates local nematic order of fibers"""
    
    print "calculating local fiber segment alignment order |", os.getcwd()

    NematicOrder=[]
    
    shape,x,y,segment_length=get_space_dimensions('')
    GridData=make_grid(FiberData,os.getcwd())

    times = sorted(GridData.keys())
    
    Nx=len(GridData[times[0]])
    Ny=len(GridData[times[0]][0])    
    
    for t in sorted(GridData):
        BoxOrder=[0]
        BoxPoints=[0]
        for xindex in range(0,Nx):
            for yindex in range(0,Ny):
                if GridData[t][xindex][yindex]!=0:
                    
                    c2=s2=0
                    Npoints=len(GridData[t][xindex][yindex])
                    for A,B,fiber in GridData[t][xindex][yindex]:
                        dx = B[0]-A[0]
                        dy = B[1]-A[1]
                        c = dx/segment_length  # cos()
                        s = dy/segment_length  # sin()
        
                        c2 += (1-2*s*s)  # c2 += cos(2a) = 1-2sin**2
                        s2 += 2*c*s      # s2 += sin(2a) = 2*cos*sin
                    BoxOrder.append(sqrt(c2**2 + s2**2)/Npoints)
                    BoxPoints.append(Npoints)
        
        LocalOrder=0
        
        
        Ntot=np.sum(BoxPoints)
                
        for a,b in zip(BoxOrder,BoxPoints):
            LocalOrder+=(a*b)/(Ntot)
        NematicOrder.append(LocalOrder)
    
    return NematicOrder
         

