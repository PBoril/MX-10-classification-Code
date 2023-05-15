# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:02:55 2023

@author: pbori
"""
import os
import numpy as np
def LoadFolder(Path):
    FilesList=os.listdir(Path)
    return(FilesList)

def LoadConfigPath():
    Pfile=open("Config.txt","r")
    ReadStr=Pfile.read()
    Pfile.close()
    return ReadStr[20:]

def CreateConfigFile(path):
    Cfile=open("Config.txt", "w")
    Cfile.write("\nLoad Folder Path = "+path+"/")
    Cfile.close()

def SaveArray(Array, ArrayName):
    Pfile="Outputs/"+ArrayName+".txt"
    np.savetxt(Pfile, Array, fmt="%.5")
    