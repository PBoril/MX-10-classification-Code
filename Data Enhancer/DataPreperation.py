# -*- coding: utf-8 -*-
"""
Created on Mon April 11 19:38:13 2023

@author: pbori
"""

import os
import numpy as np



def normalizeOne(Input):
    return (1+1/((-Input/100)-1))

def RotateArray(Input, C):
    Rot=np.rot90(Input, k=C)
    return Rot
def FlipArray(Input):
    Flip=np.flip(Input, axis=1)
    return Flip
    

def CenterAndNorm(input_array):    
    normalized_array=normalizeOne(input_array)
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

Input="output/"
Output="PrepearedData/"
    

def Transform(PathIn,PathOut, Category):
    TruePathIn=PathIn+Category
    TruePathOut=PathOut+Category
    for filename in os.listdir(TruePathIn):
        if filename.endswith('.txt'):
            input_array = np.loadtxt(os.path.join(TruePathIn, filename))
            inputArray=CenterAndNorm(input_array)
            Ar0=RotateArray(inputArray, 0)
            Ar1=RotateArray(inputArray, 1)
            Ar2=RotateArray(inputArray, 2)
            Ar3=RotateArray(inputArray, 3)
            Af0=FlipArray(Ar0)
            Af1=FlipArray(Ar1)
            Af2=FlipArray(Ar2)
            Af3=FlipArray(Ar3)
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"r0.txt"), Ar0, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"r1.txt"), Ar1, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"r2.txt"), Ar2, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"r3.txt"), Ar3, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"f0.txt"), Af0, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"f1.txt"), Af1, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"f2.txt"), Af2, fmt='%.5f')
            np.savetxt((os.path.join(TruePathOut,filename)[:-4]+"f3.txt"), Af3, fmt='%.5f')

Transform(Input, Output, "alfa")
Transform(Input, Output, "beta")
Transform(Input, Output, "gama")
Transform(Input, Output, "mion")
Transform(Input, Output, "HEP")
Transform(Input, Output, "overlap")

        
            
                
            