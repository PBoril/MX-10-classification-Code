# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter
from tkinter import *
from tkinter import filedialog as fd
import sys
from os import listdir
from os.path import isfile, join

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
R=256
C=256

root = tkinter.Tk()
root.geometry("450x300") 
root.title("Separator") 
root.option_add('*Font', 'Arial 10') 
Folder="InputData/"
FilesList = [f for f in listdir(Folder) if isfile(join(Folder, f))]
FileIndex=0
IndexNumber=tkinter.StringVar()
IndexNumber.set(FileIndex)
ObjectsArray=[]
ObjectIndex=0
ObjectNumber=tkinter.StringVar()
ObjectEnergy=tkinter.StringVar()
def execute():
    global ObjectsArray
    IndexNumber.set(FileIndex)
    print(FileIndex)
    tkinter.Label(FileManager, text="Číslo souboru="+IndexNumber.get()).grid(row=3, column=2)
    tkinter.Label(FileManager, text="Název Souboru="+FilesList[int(IndexNumber.get())]).grid(row=4, column=2)
    ShowFile(FilesList[FileIndex])
    ObjectsArray=SeparateObjects((LoadArray(FilesList[FileIndex])),0,0)
    ObjectIndex=0
def NextFile():
    global FileIndex
    FileIndex=FileIndex+1
    global ObjectIndex
    ObjectIndex=0
    execute()
def PreviousFile():
    global FileIndex
    FileIndex=FileIndex-1
    global ObjectIndex
    ObjectIndex=0
    execute()
def LoadArray(path):
    Path=Folder+path
    DataArray=[]
    SourceFile=open(Path, "r")
    for line in SourceFile:
        DataArray.append([float(x) for x in line.split()])
    SourceFile.close()
    #DataArray=np.array(DataArray)
   # DataArray=DataArray*1000
    return DataArray
def ShowFile(path):
    Path=Folder+path
    DataArray=[]
    SourceFile=open(Path, "r")
    for line in SourceFile:
            DataArray.append([float(x) for x in line.split()])
    SourceFile.close()
    plt.pcolormesh(DataArray, rasterized=True, vmin=0, vmax=np.amax(DataArray))
    plt.colorbar()
    plt.axis()
    plt.ylabel("Energie [KeV]", labelpad=-375)
    plt.show()
    return
    
def ShowObjectData(Array):
    plt.pcolormesh(Array, rasterized=True, vmin=0, vmax=np.amax(Array))
    plt.colorbar()
    plt.axis()
    plt.ylabel("Energie [KeV]", labelpad=-375)
    plt.show()
    return
def SeparateObjects(InputData, ObjectCount, threshhold):
    Support=[]
    Output=[]
    ObjectsArray=[]
    for i in range(R):
        for j in range(C):
            if InputData[i][j]<threshhold:
                InputData[i][j]=0
    for i in range(R+2):
        temp1=[]
        for j in range (C+2):
            temp1.append(0)
        Support.append(temp1)

    for i in range(R+2):
        temp2=[]
        for j in range (C+2):
            temp2.append(0)
        Output.append(temp2)
    for i in range(R):
        for j in range(C):
            if InputData[i][j]!=0:
                Support[i+1][j+1]=1
    for i in range(R):
        temp3=[]
        for j in range(C):
            temp3.append(0)
        ObjectsArray.append(temp3)
            
    detection=1
    ObjectN=1
    Hit=ObjectCount+1
    test=0
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
  
FileManager=tkinter.LabelFrame(root, text="Volba souboru")
FileManager.grid(row=1, column=1)
tkinter.Button(FileManager, command=NextFile, text=">").grid(row=2, column=3)
tkinter.Button(FileManager, command=PreviousFile, text="<").grid(row=2, column=1)
tkinter.Label(FileManager, text="Číslo souboru="+IndexNumber.get()).grid(row=3, column=2)
tkinter.Label(FileManager, text="Název Souboru="+FilesList[int(IndexNumber.get())]).grid(row=4, column=2)
def ArraySum(Array):
    X=len(Array)
    Y=len(Array[0])
    SUM=0
    for i in range (X):
        for j in range (Y):
            SUM=SUM+Array[i][j]
    return SUM
def ObjectSelected():
    global ObjectIndex
    global FileIndex
    global FileList
    global Object
    ObjectNumber.set(ObjectIndex)
    tkinter.Label(ObjectManager, text="Číslo objektu="+ObjectNumber.get()).grid(row=3, column=2)
    Object=CreateSoloObject(LoadArray(FilesList[FileIndex]),ObjectsArray, ObjectIndex)
    ShowCroppedObject(Object)
    Arr=np.array(Object)
    ObjectEnergy.set(str(round(ArraySum(Object),5))+" KeV")
    tkinter.Label(ObjectManager, text="Energie="+ObjectEnergy.get()).grid(row=4, column=2)
def Crop(Input):
    global Xmin
    global Xmax
    global Ymin
    global Ymax
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

def ShowCroppedObject(Array):
    plt.pcolormesh(Array, rasterized=True, vmin=0, vmax=np.amax(Array))
    CropRanges=Crop(Array)
    plt.xlim(CropRanges[2]-1,CropRanges[3]+2)
    plt.ylim(CropRanges[0]-1, CropRanges[1]+2)
    plt.colorbar()
    plt.ylabel("Energie [KeV]", labelpad=-375)
    plt.show()
    return
def CreateSoloObject(DataArray, ObjectArray, ObjectIndex):
    ReturnArray=[]
    for i in range(R):
        temp=[]
        for j in range(C):
            temp.append(0)
        ReturnArray.append(temp)
    for i in range(R):
        for j in range(C):
            if ObjectArray[i][j]==ObjectIndex:
                ReturnArray[i][j]=DataArray[i][j]
            else:
                ReturnArray[i][j]=0
    return ReturnArray
def NextObject():
    global ObjectIndex
    ObjectIndex=ObjectIndex+1
    ObjectSelected()
def PreviousObject():
    global ObjectIndex
    ObjectIndex=ObjectIndex-1
    ObjectSelected()

ObjectManager=tkinter.LabelFrame(root, text="Volba souboru")
ObjectManager.grid(row=1, column=2)
tkinter.Button(ObjectManager, command=NextObject, text=">").grid(row=2, column=3)
tkinter.Button(ObjectManager, command=PreviousObject, text="<").grid(row=2, column=1)
tkinter.Label(ObjectManager, text="Číslo souboru="+ObjectNumber.get()).grid(row=3, column=2)
tkinter.Label(ObjectManager, text="Energie="+ObjectEnergy.get()).grid(row=4, column=2)

def Alfa():
    global Object
    global ObjectIndex
    global FileIndex
    global FilesList
    PathFile="Output/alfa/"+(str(FilesList[FileIndex])[:-4]+"_O"+str(ObjectIndex)+".txt")
    NewFile=open(PathFile, "a")
    X=len(Object)
    Y=len(Object[0])
    for i in range (X):
        for j in range(Y):
            NewFile.write(str(Object[i][j])+" ")
        NewFile.write(str(Object[i][j])+"\n")
    NewFile.close()    
    NextObject()
def Beta():
    global Object
    global ObjectIndex
    global FileIndex
    global FilesList
    PathFile="Output/beta/"+(str(FilesList[FileIndex])[:-4]+"_O"+str(ObjectIndex)+".txt")
    NewFile=open(PathFile, "a")
    X=len(Object)
    Y=len(Object[0])
    for i in range (X):
        for j in range(Y):
            NewFile.write(str(Object[i][j])+" ")
        NewFile.write(str(Object[i][j])+"\n")
    NewFile.close()    
    NextObject()
def Gamma():
    global Object
    global ObjectIndex
    global FileIndex
    global FilesList
    PathFile="Output/gama/"+(str(FilesList[FileIndex])[:-4]+"_O"+str(ObjectIndex)+".txt")
    NewFile=open(PathFile, "a")
    X=len(Object)
    Y=len(Object[0])
    for i in range (X):
        for j in range(Y):
            NewFile.write(str(Object[i][j])+" ")
        NewFile.write(str(Object[i][j])+"\n")
    NewFile.close()    
    NextObject()
def Muion():
    global Object
    global ObjectIndex
    global FileIndex
    global FilesList
    PathFile="Output/mion/"+(str(FilesList[FileIndex])[:-4]+"_O"+str(ObjectIndex)+".txt")
    NewFile=open(PathFile, "a")
    X=len(Object)
    Y=len(Object[0])
    for i in range (X):
        for j in range(Y):
            NewFile.write(str(Object[i][j])+" ")
        NewFile.write(str(Object[i][j])+"\n")
    NewFile.close()    
    NextObject()
def HEP():
    global Object
    global ObjectIndex
    global FileIndex
    global FilesList
    PathFile="Output/HEP/"+(str(FilesList[FileIndex])[:-4]+"_O"+str(ObjectIndex)+".txt")
    NewFile=open(PathFile, "a")
    X=len(Object)
    Y=len(Object[0])
    for i in range (X):
        for j in range(Y):
            NewFile.write(str(Object[i][j])+" ")
        NewFile.write(str(Object[i][j])+"\n")
    NewFile.close()    
    NextObject()
def DROP():    
    NextObject()
def Overlap():
    global Object
    global ObjectIndex
    global FileIndex
    global FilesList
    PathFile="Output/overlap/"+(str(FilesList[FileIndex])[:-4]+"_O"+str(ObjectIndex)+".txt")
    NewFile=open(PathFile, "a")
    X=len(Object)
    Y=len(Object[0])
    for i in range (X):
        for j in range(Y):
            NewFile.write(str(Object[i][j])+" ")
        NewFile.write(str(Object[i][j])+"\n")
    NewFile.close()    
    NextObject()
Selector=tkinter.LabelFrame(root, text="Kategorie")
Selector.grid(row=2, column=1)
tkinter.Button(Selector, command=Alfa, text="Alfa").grid(row=1, column=1)
tkinter.Button(Selector, command=Beta, text="Beta").grid(row=2, column=1)
tkinter.Button(Selector, command=Gamma, text="Gamma").grid(row=3, column=1)
tkinter.Button(Selector, command=Muion, text="Mion").grid(row=4, column=1)
tkinter.Button(Selector, command=HEP, text="HEP").grid(row=5, column=1)
tkinter.Button(Selector, command=DROP, text="Přeskočit").grid(row=5, column=1)
#tkinter.Button(Selector, command=Overlap, text="Overlap").grid(row=6, column=1)


root.mainloop()
