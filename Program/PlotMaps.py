# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:28:06 2023

@author: pbori
"""

import matplotlib.pyplot as plt
import numpy as np
import DataOperations
import os

def SaveArray(Array,name):
    path="C:/finalni projekt diplomky/Python/MX-10 analyza/export"
    FilesList=os.listdir(path)
    UsedNames = [f.split(".")[0] for f in FilesList]
    Name=name
    if Name in UsedNames:
        i=1
        while f"{Name}_{i}" in UsedNames:
            i=i+1
        Name=f"{Name}_{i}.txt"
    else:
        Name = f"{Name}.txt"
    print(Name)
    fullpath=str(path+"/"+Name)
    np.savetxt(fullpath,Array,fmt="%.5f")
    
def MakePlotFromArray(Array, Cropping):
    plt.pcolormesh(Array, cmap='hot')
    if (Cropping==True):
        CropRanges=DataOperations.CropRanges(Array)
        plt.xlim(CropRanges[2]-1,CropRanges[3]+2)
        plt.ylim(CropRanges[0]-1, CropRanges[1]+2)
    plt.colorbar(label="E [KeV]")
    plt.xlabel("X [px]")
    plt.ylabel("Y [px]")
    plt.show()

def HistogramePixel(Data, Bins, Scale):
    D_pixely=np.ravel(np.array(Data))
    D_pixely = [i for i in D_pixely if i != 0]
    plt.hist(D_pixely,density=False, bins=Bins)
    plt.xlabel("Počet Pixelů")
    if (Scale==True):
        plt.xscale("log")
    plt.ylabel("Počet [n]")
    plt.grid(b=True, which="both", axis="both")
    plt.show()
    SaveArray(D_pixely, "HistPix")
    
def HistogrameEnergy(Data, Bins, Scale):
    D_pixely=np.ravel(np.array(Data))
    D_pixely = [i for i in D_pixely if i != 0]
    plt.hist(D_pixely,density=False, bins=Bins)
    plt.xlabel("Energie [KeV]")
    if (Scale==True):
        plt.xscale("log")
    plt.ylabel("Počet [n]")
    plt.grid(b=True, which="both", axis="both")
    plt.show()
    SaveArray(D_pixely, "HistEnerg") 
    
def HistogrameFunction(PType, HType, Detections, Scale,Bins):
    HistList=[]
    for k in range (len(Detections)):
        if Detections[k][3]==PType:
            HistList.append(Detections[k][HType])
        if PType==6:
            HistList.append(Detections[k][HType])
    if HType==1:
        HistogrameEnergy(HistList, Bins, Scale)
    if HType==2:
        HistogramePixel(HistList, Bins, Scale)
               
def HistogramAllFile(HType, Detections, Scale,Bins):
    HistList=[]
    for k in range(len(Detections)):
        HistList.append(Detections[k][HType])
    if HType==1:
        HistogrameEnergy(HistList, Bins, Scale)
    if HType==2:
        HistogramePixel(HistList, Bins, Scale)
        
def HistogrameDistFile(Detections):
    HistList=[0,0,0,0,0,0]
    for k in range (len(Detections)):
        for l in range(len(HistList)):
            if Detections[k][3]==l:
                HistList[l]=HistList[l]+1
    ArrayCounts={"Unknown":HistList[0], "Alpha":HistList[1],"Beta":HistList[2],"Gama":HistList[3],"Muon":HistList[4],"HEP":HistList[5]}
    Keys0=list(ArrayCounts.keys())
    Values0=list(ArrayCounts.values())
    plt.bar(Keys0,Values0)
    plt.ylabel('Počet [n]')
    plt.grid(b=True, which="both", axis="y")
    plt.show()
    SaveArray(HistList, "HistFileObjectCount") 

def ShowHCut(Array, YCord, Width):
    Input=np.array(Array)
    GraphData=[]
    GraphData=np.sum(Input[YCord:YCord+Width+1,0:],axis=0)
    for i in range(len(GraphData)):
        if GraphData[i]<0:
            GraphData[i]=0
    plt.plot(GraphData)
    plt.grid(b=True, which="both", axis="both")
    plt.xlabel("X [px]")
    plt.ylabel("E [KeV]")
    plt.show()
    SaveArray(GraphData, "Cut")
      
def PlotArray(DataArray, Yc=-1,  Xc=-1,):
    VMAX=np.amax(DataArray)
    if Xc>0:
        plt.axhline(y=Xc, color='g', linestyle='dotted')
    if Yc>-1:
        plt.axhline(y=Yc, color='g', linestyle='dotted')
    for i in range(len(DataArray)):
        for j in range(len(DataArray[0])):
            if DataArray[i][j]<0:
                DataArray[i][j]=0
    plt.pcolormesh(DataArray, rasterized=True, vmin=0, vmax=VMAX,cmap='hot')
    plt.colorbar(label="E [KeV]")
    plt.xlabel("X [px]")
    plt.ylabel("Y [px]")
    plt.show()
    return