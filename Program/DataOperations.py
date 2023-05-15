# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:28:52 2023

@author: pbori
"""

import numpy as np
import Analysis




def MakeArrayFromFile(Folder, File):
    path=Folder+"/"+File
    FileArray = np.loadtxt(path, comments="#", delimiter=" ", unpack=False)
    return FileArray
    

def SeparateObjects(InputData):
    Support=[]
    Output=[]
    ObjectsArray=[]
    R=len(InputData)
    C=len(InputData[0])
    for i in range(R+2):
        temp1=[]
        for j in range (C+2):
            temp1.append(0)
        Support.append(list(temp1))

    for i in range(R+2):
        temp2=[]
        for j in range (C+2):
            temp2.append(0)
        Output.append(list(temp2))
    for i in range(R):
        for j in range(C):
            if InputData[i][j]!=0:
                Support[i+1][j+1]=1
    for i in range(R):
        for j in range(C):
            if InputData[i][j]!=0:
                Support[i+1][j+1]=1
    for i in range(R):
        temp3=[]
        for j in range(C):
            temp3.append(0)
        ObjectsArray.append(list(temp3))
    ObjectN=0
    detection=1
    ObjectN=1
    Hit=1
    while detection!=0:
        detection=0
        Found=0
        for i in range (R):
            for j in range(C):                
                x=i+1
                y=j+1
            
                if Found==0:
                    if Support[x][y]==1:
                        Support[x][y]=2
                        detection=1
                        Found=1
        while ObjectN!=0:
                ObjectN=0
                for i in range (R):
                    for j in range(C):
                        x=i+1
                        y=j+1
                        if Support[x][y]==2:
                    
                            if Support[x-1][y-1]==1:
                                Support[x-1][y-1]=2
                                ObjectN=1
                            
                            if Support[x-1][y]==1:
                                Support[x-1][y]=2
                                ObjectN=1
                            
                            if Support[x-1][y+1]==1:
                                Support[x-1][y+1]=2
                                ObjectN=1
                            
                            if Support[x][y-1]==1:
                                Support[x][y-1]=2
                                ObjectN=1
                            
                            if Support[x][y+1]==1:
                                Support[x][y+1]=2
                                ObjectN=1
                            
                            if Support[x+1][y-1]==1:
                                Support[x+1][y-1]=2
                                ObjectN=1
                            
                            if Support[x+1][y]==1:
                                Support[x+1][y]=2
                                ObjectN=1
                            
                            if Support[x+1][y+1]==1:
                                Support[x+1][y+1]=2
                                ObjectN=1
                if ObjectN==0:
                    for i in range(R):
                        for j in range(C):
                            x=i+1
                            y=j+1                    
                            if Support[x][y]==2:
                                test=1
                                Support[x][y]=0
                                Output[x][y]=Hit
                                if test==0:
                                    test=1
                                    ObjectN=1
        for i in range(R):
            for j in range(C):
                if ObjectN==0:
                    x=i+1
                    y=j+1
                    if Support[x][y]!=0:
                        detection=1
                        ObjectN=1
                        Hit=Hit+1
    for i in range(R):
        for j in range(C):
            ObjectsArray[i][j]=Output[i+1][j+1]
    
    
    return ObjectsArray

def MakeObjectArray(Array, ObjectArray, ID):
    Object=np.zeros((len (Array),len (Array[0])))
    for i in range(len (Array)):
        for j in range(len (Array[0])):
            if ObjectArray[i][j]==ID:
                Object[i][j]=Array[i][j]
    return Object



def CenterObject(Array, ObjectArray, ID):
    Object=MakeObjectArray(Array, ObjectArray, ID)
    CenteredObject=np.zeros((len(Object),len(Object[0])))
    Mean=np.nonzero(Object)
    RMean=round(np.mean(Mean[0]))
    CMean=round(np.mean(Mean[1]))
    RHalf=round(len(Object)/2)-RMean
    CHalf=round(len(Object[0])/2)-CMean
    CenterObj = np.roll(Object, int(RHalf), axis=0)
    CenterObj = np.roll(CenterObj, int(CHalf), axis=1)
    CenterObj=CenterObj/np.sum(CenterObj)
    return CenterObj


def MakeArraySingleCategory(Array,ObjectArray,Detections,Category):
    ArrayOut=np.zeros((len(Array),len(Array[0])))
    for i in range(len(Array)):
        for j in range(len(Array[0])):
            for k in range(len(Detections)):
                if Detections[k][3]==Category:
                    if ObjectArray[i][j]==(k+1):
                        ArrayOut[i][j]=Array[i][j]
    return ArrayOut
    



def normalizeSize(Input):
    return (1+1/((-Input/100)-1))

def NormalizeObjectNN(input_array):
    Normalize=np.array(input_array)
    normalized_array=normalizeSize(Normalize)
    nonzero_indices = np.nonzero(normalized_array)
    center = np.array([np.mean(nonzero_indices[0]), np.mean(nonzero_indices[1])])
    offset = np.array([normalized_array.shape[0]/2, normalized_array.shape[1]/2]) - center
    output_array= np.roll(normalized_array, int(offset[0]), axis=0)
    output_array= np.roll(output_array, int(offset[1]), axis=1)
    Resize_array=np.zeros((256,256))
    for i in range(256):
        for j in range(256):
            Resize_array[i][j]=output_array[i][j]
    
    return Resize_array

    

def CropRanges(Input):
    R=len(Input)
    C=len(Input[0])
    
    Rmin=R+1
    Cmin=C+1
    Rmax=0
    Cmax=0
    Output=[]
    for i in range (R):
        for j in range (C):
            if Input[i][j]!=0:
                if i<Rmin:
                    Rmin=i
                if j<Cmin:
                    Cmin=j
                if i>Rmax:
                    Rmax=i
                if j>Cmax:
                    Cmax=j
    return(Rmin, Rmax, Cmin, Cmax)

