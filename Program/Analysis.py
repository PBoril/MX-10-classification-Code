# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 18:48:14 2023

@author: pbori
"""
import numpy as np
import DataOperations
from skimage.feature import peak_local_max
def TotalEnergy(Array):
    return np.sum(Array)

def TotalPixels(Array):
    return np.count_nonzero(Array)

def Saturation(Array):
    TotalPx=len(Array)*len(Array[0])
    UsedPx=TotalPixels(Array)
    return UsedPx/TotalPx

def FileAnalysis(Array, Model):
    Array=np.array(Array)
    Array=np.resize(Array, (256,256))
    ObjectsArray=DataOperations.SeparateObjects(Array)
    DetectionList=[]    #ID, Energy, Pixel, Type, Certainty
    for l in range (np.amax(ObjectsArray)):
        Temp=[l,0,0,0, 0]
        DetectionList.append(Temp)
    for k in range (len(DetectionList)):
        for i in range (len(Array)):
            for j in range (len (Array)):
                if ObjectsArray[i][j]==(k+1):
                    DetectionList[k][2]=DetectionList[k][2]+1
                    DetectionList[k][1]=DetectionList[k][1]+Array[i][j]
    for k in range(len(DetectionList)):
        Classed=NNClass(Model, DataOperations.MakeObjectArray(Array, ObjectsArray, k+1))
        DetectionList[k][3]=Classed[0]
        DetectionList[k][4]=round((Classed[1])*100,5)
    return DetectionList, ObjectsArray

def NNClass(model, array):     
    Arr=DataOperations.NormalizeObjectNN(array)
    #categories = ['Alfa', 'Beta', 'Gama','Muon','Overlap']
    predicted_class = model.predict(np.reshape(Arr,(1,256,256,1)),verbose = 0)
    predicted_category = np.argmax(predicted_class)+1
    certainty=predicted_class[0][np.argmax(predicted_class)]
    if (certainty<0.60):                #Hraniční jistota pro klasifikaci
        predicted_category=0
    if np.sum(array)>7500:              #Hraniční hodnota energie pro HEP
        predicted_category=5
        certainty=1
    if np.sum(array)>4000:              #Hraniční hodnota pro HEP s kritérii na počet lokálních maxim
        PeaksC=[]
        PeaksC=peak_local_max(array)
        if (len(PeaksC)>1):
            PeaksV=np.zeros((len(PeaksC)))
            for P in range(len(PeaksC)):
                X=PeaksC[P][0]
                Y=PeaksC[P][1]
                PeaksV[P]=array[X,Y]
            PeaksM=np.amax(PeaksV)
            for K in range(len(PeaksV)):
                if (PeaksV[K]>(PeaksM*0.35)):
                    predicted_category=5
                    certainty=1
    return predicted_category, certainty