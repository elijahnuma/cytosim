#!/usr/bin/env python
"""
    
   Collection of functions to extract information from cytosim simulation data
    
"""


from math import *
import os, sys
#from Pillow import Image
from copy import deepcopy
import time

#=========================================================================

def read_fiber_straightness(dir):
    """returns dictionary with straightness of all fibers"""
    
    print "reading fibers straightness |", dir
    
    global FiberStraight
    FiberStraight={} # Fiber straightness:  FiberStraight[time][id] = straightness

    FileName = 'FiberStraight.dat'
    if (not os.path.isfile(FileName)): os.system('report fiber > ' + FileName)
    File=open(FileName,'r')

    for line in File.readlines():
        if len(line)>1 and line[0]!='w':
            
            if line.split()[1] in ['time','start']:
                t=float(line.split()[2]) #recording time
                FiberStraight[t]={}
            
            elif line.split()[0]!='%':
                if len(line.split())==9:
                    cl, id, l, x, y, dx, dy, ee, cs =  line.split()
                elif len(line.split())==8:
                    cl, id, l, x, y, dx, dy, ee  =  line.split()

                id=int(id); l=float(l); ee=float(ee)

                FiberStraight[t][id] = ee/l  # end-to-end distance / length
    
    File.close()

    return FiberStraight

#-------------------------------------------------------------------------

def read_fiber_CM(dir):
    """returns dictionary with fibers center of mass"""
    
    print "reading fibers center of masses |", dir, os.getcwd()
    
    global FiberCM
    FiberCM={} # Fiber Center of mass:  FiberCM[time][id] = [x,y]
    
    FileName = 'FiberCM.dat'
    if (not os.path.isfile(FileName)): os.system('report fiber > ' + FileName)
    File=open(FileName,'r')
    
    for line in File.readlines():
        if len(line)>1 and line[0]!='w':
            
            if line.split()[1] in ['time','start']:
                t=float(line.split()[2]) #recording time
                FiberCM[t]={}
            
            elif line.split()[0]!='%':
                if len(line.split())==9:
                    cl, id, l, x, y, dx, dy, ee, cs =  line.split()
                elif len(line.split())==8:
                    cl, id, l, x, y, dx, dy, ee  =  line.split()
                else:
                    cl, id, l, x, y, dx, dy  =  line.split()
                
                id=int(id); x=float(x); y=float(y)

                FiberCM[t][id]=[x,y]

    File.close()

    return FiberCM

#-------------------------------------------------------------------------

def read_fiber_points(dir):
    """returns dictionary with fibers center of mass"""

    
    originalpath=os.getcwd()
    if dir != '':    
        os.chdir(dir)
    
    print "reading fibers list of points |", dir
    
    
    global FiberPts
    FiberPts={} # Fiber Points:  FiberPts[time][id] = [ [x,y] ]
    
    FileName = 'FiberPoints.dat'

    if (os.path.isfile(FileName)): 
        os.remove('FiberPoints.dat')        
        os.system('report fiber:point > ' + FileName)
    if (not os.path.isfile(FileName)): 
        os.system('report fiber:point > ' + FileName)
    File=open(FileName,'r')
    
    for line in File.readlines():
        if len(line)>1 and line[0]!='w':
            
            if line.split()[1] in ['time','start']:
                t = float(line.split()[2]) #recording time
                FiberPts[t]={}
            
            elif line.split()[1]=='fiber':
                id = int(line.split(':')[-1].split()[0])
                FiberPts[t][id]=[]
            
            elif line.split()[0]!='%':
                id, x, y  =  line.split()
                id=int(id); x=float(x); y=float(y)
                FiberPts[t][id].append([x,y])

    File.close()
    os.chdir(originalpath)
    
    return FiberPts

#=========================================================================

def read_couples(dir):
    """get the name of all couples and store their positions in time"""

    originalpath=os.getcwd()
    if dir != '':    
        os.chdir(dir)
    
    print "reading couples names + positions |", dir
    
    CouplesNames=[] # Couple names:      CouplesNames = [names]
    Couples={}      # Couple positions:  Couples[names][t][id] = [x,y]
    
    # - NAMES - - - - - - - - - - - - - - - - - - - -
    FileName = 'Couples.dat'
    if not os.path.isfile(FileName): os.system('report couple > ' + FileName)
    File = open(FileName,'r')
    
    for line in File.readlines():
        if len(line)>1 and line[0]!='w' and line[0]!='%':
            
            name = line.split()[0]
            if name in CouplesNames: break
            CouplesNames.append(name)

    File.close()

    # - POSITIONS - - - - - - - - - - - - - - - - - -
    for couple in CouplesNames:
        FileName = 'Couples-'+couple+'.dat'
        if (not os.path.isfile(FileName)): os.system('report couple:'+couple+' > ' + FileName)
        File = open(FileName,'r')
        
        Couples[couple]={}
        for line in File.readlines():
            if len(line)>1 and line[0]!='w':
                
                if line.split()[1] in ['time','start']:
                    t=float(line.split()[2]) #recording time
                    Couples[couple][t]={}
                
                elif line.split()[0]!='%':
                    if len(line.split())>7:
                        cl, id, act, x, y, f1, f1abs, f2, f2abs = line.split()
                    else:
                        cl, id, st, act, x, y, z = line.split()
                        f1,f1abs,f2,f2abs=0
                    id = int(id); x = float(x); y=float(y); f1=int(f1); f1abs=float(f1abs); f2=int(f2); f2abs=float(f2abs);

                    Couples[couple][t][id]=[x,y,f1,f1abs,f2,f2abs]

        File.close()

    os.chdir(originalpath)
    return Couples

#-------------------------------------------------------------------------

def read_singles(dir):
    """get the name of all singles and store their positions in time"""
    
    print "reading single names + positions |", dir, os.getcwd()
    
    SinglesNames=[] # Single names:      SinglesNames = [names]
    Singles={}      # Single positions:  Singles[names][t][id] = [x,y]
    
    # - NAMES - - - - - - - - - - - - - - - - - - - -
    FileName = 'Singles.dat'
    if not os.path.isfile(FileName): os.system('report singles:force > ' + FileName)
    File = open(FileName,'r')
  

    # - POSITIONS - - - - - - - - - - - - - - - - - -

        
    Singles={}
    for line in File.readlines():
        if len(line)>1 and line[0]!='w':
                
            if line.split()[1] in ['time','start']:
                t=float(line.split()[2]) #recording time
                Singles[t]={}
            
            elif line.split()[0]!='%':
                if len(line.split())>7:
                    cl, id, x, y, fx, fy, f, fabs, ast = line.split()
                else:
                    cl, id, st, act, x, y, z = line.split()
                id = int(id); x = float(x); y=float(y)
                   
                Singles[t][id]=[x,y,fabs]
        
        File.close()

    return Singles

#=========================================================================

def get_space_dimensions(dir):
    """reads and returns the space dimensions"""

    if dir != '':    
        os.chdir(dir)    

    FileName = 'Parameters.dat'
    if (not os.path.isfile(FileName)): os.system('report parameters > ' + FileName)
    File=open(FileName,'r')   
    
    shape=x=y=segmentation=0
    for line in File.readlines():

        if line.startswith(' shape'):
            shape = line.split()[2][:-1]
    
        elif line.startswith(' dimensions'):
            line2 = line.split()
            if len(line2)>3:
                x, y = float(line2[2]), float(line2[3][:-1])
            else:
                x = y = float(line2[2][:-1])
        elif line.startswith(' segmentation'):
            segmentation = float(line.split()[2][:-1])
            return shape,x,y,segmentation    

    if shape==0:
        print 'ERROR: information about shape and dimensions not found'
        return shape, x, y, segmentation

#=========================================================================


def make_grid(FiberPts,dir):
    """divides space into small boxes of length <space>"""

    originalpath=os.getcwd()
    if dir != '':    
        os.chdir(dir)    

    print """divides space into small boxes of length <space>"""

    global BOXS, nb_fibers
        
    shape, xdim, ydim, segmentation = get_space_dimensions(dir)
    
    segmentation*=2
    
    morespace=1
    
    nbX = int(xdim*2.*morespace/segmentation+2) #number of boxes in each direction
    nbY = int(ydim*2.*morespace/segmentation+2)
    
    print nbX

    BOXS={}
    for t in FiberPts:
        BOXS[t]={}
        BOXS[t]= [ [0]*nbY for x in range(nbX) ] # BOXS[y][x]
    
    
    for t in FiberPts:
        for fiber in FiberPts[t]:
                
            for A,B in zip(FiberPts[t][fiber],FiberPts[t][fiber][1:]): #A[x,y],B[x,y] = coordinates of segments

                x, y = A[0], A[1]
                    
                xx = int( (x+xdim*morespace)/segmentation )%nbX
                yy = int( (y+ydim*morespace)/segmentation )%nbY

                

                if BOXS[t][xx][yy]==0:
                    BOXS[t][xx][yy]=[]
                BOXS[t][xx][yy].append([A,B,fiber])
        
        nb_fibers = len(FiberPts[t])
    return BOXS


def get_number_of_intersections(t):
    """counting the number of fiber intersections and sotring position along fiber"""

    global FiberIntersections
    
    FiberIntersections={} # FiberIntersections[id]=[abcissa of intersection]
    
    N_intersections=0
    
    for x in range(1,len(BOXS[0])):
        for y in range(1,len(BOXS)):
            if (BOXS[x][y] !=0):
                    
                for xx in range(x-1,x+2):
                    for yy in range(y-1,y+2):
                        if (BOXS[xx][yy] !=0):
                                
                            for A,B,fib in BOXS[x][y]:
                                for C,D,fib2 in BOXS[xx][yy]:
                                    if fib>fib2:
                                        n,px,py = lineIntersection(A,B,C,D)
                                        N_intersections += n
                                        
                                        if fib not in FiberIntersections:
                                            FiberIntersections[fib]=[]
                                        x0,y0 = FiberPts[t][fib][0]
                                        if abs(x0)<5 and abs(y0)<5:
                                            L=sqrt((x0-px)**2+(y0-py)**2)
                                            if L not in FiberIntersections[fib]:
                                                FiberIntersections[fib].append(L)

                                        if fib2 not in FiberIntersections:
                                            FiberIntersections[fib2]=[]
                                        x0,y0 = FiberPts[t][fib2][0]
                                        if abs(x0)<5 and abs(y0)<5:
                                            L=sqrt((x0-px)**2+(y0-py)**2)
                                            if L not in FiberIntersections[fib2]:
                                                FiberIntersections[fib2].append(L)

    return N_intersections, N_intersections*1.0/nb_fibers


def lineIntersection(A, B, C, D):
    """algorithm to check if two segments intersect"""

    Bx_Ax = B[0] - A[0]; By_Ay = B[1] - A[1]
    Dx_Cx = D[0] - C[0]; Dy_Cy = D[1] - C[1]

    determinant = (-Dx_Cx*By_Ay + Bx_Ax*Dy_Cy)

    if abs(determinant) < 1e-20: return 0, 0,0 #None

    s = (-By_Ay*(A[0] - C[0]) + Bx_Ax*(A[1] - C[1])) / determinant
    t = ( Dx_Cx*(A[1] - C[1]) - Dy_Cy*(A[0] - C[0])) / determinant
    if (s>=0 and s<=1 and t>=0 and t<=1):
        return 1, A[0]+(t*Bx_Ax), A[1]+(t*By_Ay)

    return 0,0,0

#=========================================================================
