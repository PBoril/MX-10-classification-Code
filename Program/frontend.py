import tkinter as tk
from tkinter import filedialog
import InputsOutputs
import PlotMaps
import DataOperations
import matplotlib.pyplot as plt
import Analysis
from tensorflow import keras
import numpy as np
import os
from scipy.ndimage import interpolation
import warnings

warnings.simplefilter('ignore', category=DeprecationWarning)
modelF= keras.models.load_model('Model4BLSTM.h5')       #Cesta k modelu o čtyřech kategoriích
modelC=keras.models.load_model('Model3_BLSTM.h5')       #Cesta k modelu o třech kategoriích

#Main setup
root = tk.Tk()
root.title("MX-10 Viewer")
root.geometry("1280x720")

#DECLARED VARIABLES
TkBins=tk.IntVar()
TKMuons=tk.BooleanVar()
TkFolderPath=tk.StringVar()
TkFileIndex=tk.IntVar()
TkFileMaxIndex=tk.IntVar()
TkCrop=tk.IntVar()
TkFileName=tk.StringVar()
TkObjectMax=tk.IntVar()
TkObjectIndex=tk.IntVar()
TkLOG=tk.BooleanVar()
ListOfFiles=[]
Detections=[]
ObjectsArray=[]

#TEMPORAL VARIABLES
Classes=['   Alfa   ','   Beta   ','   Gama   ','   Mion   ','   HEP   ','Neznámá']     #kategorie

#FolderInfo
AllParticleCountFolder=tk.IntVar()
AlphaCountFolder=tk.IntVar()
BetaCountFolder=tk.IntVar()
GamaCountFolder=tk.IntVar()
MuonCountFolder=tk.IntVar()
HEPCountFolder=tk.IntVar()
UnknownCountFolder=tk.IntVar()
TotalEnergyCountFolder=tk.DoubleVar()
AverageSaturationFolder=tk.DoubleVar()

#FileInfo
AllParticleCountFile=tk.IntVar()
AlphaCountFile=tk.IntVar()
BetaCountFile=tk.IntVar()
GamaCountFile=tk.IntVar()
MuonCountFile=tk.IntVar()
HEPCountFile=tk.IntVar()
UnknownCountFile=tk.IntVar()
TotalEnergyCountFile=tk.DoubleVar()
SaturationFile=tk.DoubleVar()
  
#ObjectInfo
ObjectEnergy=tk.DoubleVar()
ObjectSize=tk.IntVar()
ObjectType=tk.StringVar()
TKObjectCertainty=tk.DoubleVar()

def FolderSelect():
    FolderPath=filedialog.askdirectory(title="Zvol složku s daty")
    TkFolderPath.set(FolderPath)
    RefreshFolderFrame()
    FolderFilesList=InputsOutputs.LoadFolder(FolderPath)
    TkFileMaxIndex.set(len(FolderFilesList))
    RefreshFileFrame()
    global ListOfFiles
    ListOfFiles=FolderFilesList
    InputsOutputs.CreateConfigFile(FolderPath)

def ShowRawFile():
    global ListOfFiles
    PlotMaps.MakePlotFromArray(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]),TkCrop.get())

def ShowSingleObject():
    global ObjectsArray
    PlotMaps.MakePlotFromArray(DataOperations.MakeObjectArray(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]),ObjectsArray,TkObjectIndex.get()),TkCrop.get())
        
def UpdateFileFrame():
    TotalEnergyCountFile.set(str(round(float(Analysis.TotalEnergy(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]))),2)))
    SaturationFile.set(str(round(100*float(Analysis.Saturation(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]))),3)))
    RefreshFileFrame()

def emptyfunction():
    print("#")
def RefreshFolderFrame():
    tk.Label(FolderFrame, text="cesta k souboru: \n "+TkFolderPath.get()).grid(row=10, column=10)

def RefreshFileFrame():
    global ListOfFiles
    tk.Label(FileFrame, text="Soubor "+str(TkFileIndex.get())+"/"+str(TkFileMaxIndex.get())+"\n"+TkFileName.get()).grid(row=10, column=10)
    RefreshFileInfoFrame()  
    
def RefreshObjectFrame():
    tk.Label(ObjectFrame, text="Objekt: "+str(TkObjectIndex.get())+"/"+str(TkObjectMax.get())).grid(row=10, column=10)
    
def FileIDAdd():
    if (TkFileIndex.get()<TkFileMaxIndex.get()):
        TkFileIndex.set(TkFileIndex.get()+1)
        ShowRawFile()
        TkFileName.set(ListOfFiles[TkFileIndex.get()-1])
        UpdateFileFrame()
        
def FileIDSub():
    if (TkFileIndex.get()>1):
        TkFileIndex.set(TkFileIndex.get()-1)
        ShowRawFile()
        TkFileName.set(ListOfFiles[TkFileIndex.get()-1])
        UpdateFileFrame()
        
def FileIDSelect():
    if ((int(FileID.get())>0) and (int(FileID.get())<=int(TkFileMaxIndex.get()))):
        TkFileIndex.set(FileID.get())
        ShowRawFile()
        TkFileName.set(ListOfFiles[TkFileIndex.get()-1])
        UpdateFileFrame()
        
def RefreshFolderInfoFrame():
    tk.Label(FolderInfoFrame, text="počet všech částic: "+str(AllParticleCountFolder.get())).grid(row=5, column=10)
    tk.Label(FolderInfoFrame, text="počet částic alfa: "+str(AlphaCountFolder.get())).grid(row=10, column=10)
    tk.Label(FolderInfoFrame, text="počet částic beta: "+str(BetaCountFolder.get())).grid(row=20, column=10)
    tk.Label(FolderInfoFrame, text="počet částic gama: "+str(GamaCountFolder.get())).grid(row=30, column=10)
    tk.Label(FolderInfoFrame, text="počet mionů: "+str(MuonCountFolder.get())).grid(row=40, column=10)
    tk.Label(FolderInfoFrame, text="počet HEP: "+str(HEPCountFolder.get())).grid(row=50, column=10)
    tk.Label(FolderInfoFrame, text="počet neznámých částic: "+str(UnknownCountFolder.get())).grid(row=60, column=10)
    tk.Label(FolderInfoFrame, text="celková detekovaná energie: "+str(TotalEnergyCountFolder.get())+" MeV").grid(row=70, column=10)
    tk.Label(FolderInfoFrame, text="Průměrná saturace: "+str(AverageSaturationFolder.get())+"%").grid(row=80, column=10)        
        
def RefreshFileInfoFrame():
    tk.Label(FileInfoFrame, text="počet všech částic: "+str(AllParticleCountFile.get())).grid(row=5, column=10)
    tk.Label(FileInfoFrame, text="počet částic alfa: "+str(AlphaCountFile.get())).grid(row=10, column=10)
    tk.Label(FileInfoFrame, text="počet částic beta: "+str(BetaCountFile.get())).grid(row=20, column=10)
    tk.Label(FileInfoFrame, text="počet částic gama: "+str(GamaCountFile.get())).grid(row=30, column=10)
    tk.Label(FileInfoFrame, text="počet mionů: "+str(MuonCountFile.get())).grid(row=40, column=10)
    tk.Label(FileInfoFrame, text="počet HEP: "+str(HEPCountFile.get())).grid(row=50, column=10)
    tk.Label(FileInfoFrame, text="počet neznámých částic: "+str(UnknownCountFile.get())).grid(row=60, column=10)
    tk.Label(FileInfoFrame, text="celková detekovaná energie: "+str(TotalEnergyCountFile.get())+" KeV").grid(row=70, column=10)
    tk.Label(FileInfoFrame, text="saturace: "+str(SaturationFile.get())+"%").grid(row=80, column=10)
    
def RefreshObjectInfoFrame():
    tk.Label(ObjectInfoFrame, text="detekovaná energie objektu: "+str(round(float(ObjectEnergy.get()),3))+" KeV").grid(row=10, column=10)
    tk.Label(ObjectInfoFrame, text="počet pixelů objektu: "+str(ObjectSize.get())).grid(row=20, column=10)
    tk.Label(ObjectInfoFrame, text="typ objektu: "+str(ObjectType.get())).grid(row=30, column=10)    
    tk.Label(ObjectInfoFrame, text="jistota: "+str(TKObjectCertainty.get())+" %").grid(row=40, column=10)  

def ObjectIDAdd():
    global Detections
    if (TkObjectIndex.get()<TkObjectMax.get()):
        TkObjectIndex.set(TkObjectIndex.get()+1)
        RefreshObjectFrame()
        ObjectEnergy.set(Detections[TkObjectIndex.get()-1][1])
        ObjectSize.set(Detections[TkObjectIndex.get()-1][2])
        ObjectType.set(Classes[Detections[TkObjectIndex.get()-1][3]-1])
        TKObjectCertainty.set(Detections[TkObjectIndex.get()-1][4])
        RefreshObjectInfoFrame()
        ShowSingleObject()
        
def ObjectIDSub():
    global Detections
    if (TkObjectIndex.get()>1):
        TkObjectIndex.set(TkObjectIndex.get()-1)
        RefreshObjectFrame()
        ObjectEnergy.set(Detections[TkObjectIndex.get()-1][1])
        ObjectSize.set(Detections[TkObjectIndex.get()-1][2])
        ObjectType.set(Classes[Detections[TkObjectIndex.get()-1][3]-1])
        TKObjectCertainty.set(Detections[TkObjectIndex.get()-1][4])
        RefreshObjectInfoFrame()
        ShowSingleObject()
        
def ObjectIDSelect():
    global Detections
    if ((int(ObjectID.get())>0) and (int(ObjectID.get())<=int(TkObjectMax.get()))):
        TkObjectIndex.set(ObjectID.get())
        RefreshObjectFrame()
        ObjectEnergy.set(Detections[TkObjectIndex.get()-1][1])
        ObjectSize.set(Detections[TkObjectIndex.get()-1][2])
        ObjectType.set(Classes[Detections[TkObjectIndex.get()-1][3]-1])
        TKObjectCertainty.set(Detections[TkObjectIndex.get()-1][4])
        RefreshObjectInfoFrame()
        ShowSingleObject()

def FileInfo():
    global Detections
    global ObjectsArray
    if (TKMuons.get()==True):
        model=modelF
    if (TKMuons.get()==False):
        model=modelC
    DetectionFunction=Analysis.FileAnalysis(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]),model)
    Detections=DetectionFunction[0]
    ObjectsArray=DetectionFunction[1]
    AllParticleCountFile.set(len(Detections))
    TkObjectMax.set(AllParticleCountFile.get())
    Counts=[0,0,0,0,0,0,0]
    for k in range (len(Counts)):
        for l in range (len(Detections)):
            if Detections[l][3]==k:
                Counts[k]=Counts[k]+1
    AlphaCountFile.set(Counts[1])
    BetaCountFile.set(Counts[2])
    GamaCountFile.set(Counts[3])
    MuonCountFile.set(Counts[4])
    HEPCountFile.set(Counts[5])
    UnknownCountFile.set(Counts[0])
    RefreshFileFrame()
    RefreshObjectFrame()
    np.savetxt("detections/File_"+str(TkFileIndex.get()-1)+".txt",Detections, fmt="%.5f")
    TkBins.set(100)
    tk.Button(GraphPlotFrameFile, command=HistEnergyAllFile, text="energii", state='normal').grid(row=10,column=10)
    tk.Button(GraphPlotFrameFile, command=HistPixAllFile, text="velikosti", state='normal').grid(row=20,column=10)
    tk.Button(GraphPlotFrameFile, command=HistTypeDistributionFile, text="zastoupeni typu", state='normal').grid(row=30,column=10)
    tk.Button(GraphPlotFrameFile, command=HistFileEnergyAlpha, text="energii alfa", state='normal').grid(row=40,column=10)
    tk.Button(GraphPlotFrameFile, command=HistFileEnergyBeta, text="energii beta", state='normal').grid(row=50,column=10)
    tk.Button(GraphPlotFrameFile, command=HistFileEnergyGama, text="energii gama", state='normal').grid(row=60,column=10)
    tk.Button(GraphPlotFrameFile, command=HistFileEnergyMuon, text="energii mionu", state='normal').grid(row=70,column=10)
    tk.Button(GraphPlotFrameFile, command=HistFileEnergyHEP, text="energii HEP", state='normal').grid(row=80,column=10)
    tk.Button(ObjectSelectFrame,command=ShowAlpha, text="alfa", state="normal").grid(row=10,column=10,sticky="nsew")
    tk.Button(ObjectSelectFrame,command=ShowBeta, text="beta", state="normal").grid(row=20,column=10,sticky="nsew")
    tk.Button(ObjectSelectFrame,command=ShowGama, text="gama", state="normal").grid(row=30,column=10,sticky="nsew")
    tk.Button(ObjectSelectFrame,command=ShowMuon, text="miony", state="normal").grid(row=40,column=10,sticky="nsew")
    tk.Button(ObjectSelectFrame,command=ShowHEP, text="HEP", state="normal").grid(row=50,column=10,sticky="nsew")
    tk.Button(ObjectFrame, text="<", command=ObjectIDSub, state="normal").grid(row=30, column=5)
    tk.Button(ObjectFrame, text="Zvolit", command=ObjectIDSelect, state="normal").grid(row=30, column=10)
    tk.Button(ObjectFrame, text=">", command=ObjectIDAdd, state="normal").grid(row=30, column=15)

def FolderInfo():
    global FolderDetections
    global FolderInputFiles
    global FolderObjectsArray
    global AllDetections
    if (TKMuons.get()==True):
        model=modelF
    if (TKMuons.get()==False):
        model=modelC
    FolderInputFiles=[]
    FolderDetections=[]
    FolderDetectionFunction=[]
    for k in range (len(ListOfFiles)):
        FolderInputFiles.append(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[k]))
        FolderDetectionFunction.append(Analysis.FileAnalysis(FolderInputFiles[k],model))
        FolderDetections.append(FolderDetectionFunction[k][0])
        print('File '+str(k+1)+"/"+str(len(ListOfFiles))+" Done")
    AllDetections=np.concatenate(FolderDetections, axis=0, )
    for l in range(len(AllDetections)):
        AllDetections[l][0]=l
    CountsFolder=[0,0,0,0,0,0,0]
    for i in range (len(CountsFolder)):
        for j in range (len(AllDetections)):
            if AllDetections[j][3]==i:
                CountsFolder[i]=CountsFolder[i]+1
    AllParticleCountFolder.set(len(AllDetections))
    AlphaCountFolder.set(CountsFolder[1])
    BetaCountFolder.set(CountsFolder[2])
    GamaCountFolder.set(CountsFolder[3])
    MuonCountFolder.set(CountsFolder[4])
    HEPCountFolder.set(CountsFolder[5])
    UnknownCountFolder.set(CountsFolder[0])
    TotalPixels=0
    TotalEnergy=0
    for E in range(len(AllDetections)):
        TotalEnergy=TotalEnergy+AllDetections[E][1]
    TotalEnergyCountFolder.set(round((TotalEnergy/1000),3))
    for P in range(len(AllDetections)):
        TotalPixels=TotalPixels+AllDetections[P][2]
    AverageSaturationFolder.set(str(round(100*(TotalPixels/(len(ListOfFiles)*256*256)),3)))
    RefreshFolderInfoFrame()
    np.savetxt("detections/Folder.txt",AllDetections, fmt="%.5f")
    TkBins.set(100)
    tk.Button(GraphPlotFrameFolder, command=HistEnergyAllFolder, text="energii", state='normal').grid(row=10,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistPixAllFolder, text="velikosti", state='normal').grid(row=20,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistTypeDistributionFolder, text="zastoupeni typu", state='normal').grid(row=30,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyAlpha, text="energii alfa", state='normal').grid(row=40,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyBeta, text="energii beta", state='normal').grid(row=50,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyGama, text="energii gama", state='normal').grid(row=60,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyMuon, text="energii mionu", state='normal').grid(row=70,column=10)
    tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyHEP, text="energii HEP", state='normal').grid(row=80,column=10)

#SELECTORS
#Folders
FolderFrame=tk.LabelFrame(root,text="Volba složky",pady=5, padx=5)
FolderFrame.grid(row=10, column=10)
RefreshFolderFrame()
tk.Button(FolderFrame, text="Vybrat", command=FolderSelect).grid(row=20, column=10)
tk.Button(FolderFrame, text="Analýza", command=FolderInfo).grid(row=30, column=10)
#Files
FileFrame=tk.LabelFrame(root,text="Volba souboru", pady=5, padx=5)
FileFrame.grid(row=20, column=10)

FileID=tk.Entry(FileFrame, width=8)
FileID.grid(row=20,column=10)
tk.Button(FileFrame, text="<", command=FileIDSub).grid(row=30, column=5)
tk.Button(FileFrame, text="Zvolit", command=FileIDSelect).grid(row=30, column=10)
tk.Button(FileFrame, text=">", command=FileIDAdd).grid(row=30, column=15)
tk.Button(FileFrame, text="Analýza", command=FileInfo).grid(row=40, column=10)

#Objects
ObjectFrame=tk.LabelFrame(root, text="Detekce", pady=5, padx=5)
ObjectFrame.grid(row=30, column=10)

ObjectID=tk.Entry(ObjectFrame, width=8)
ObjectID.grid(row=20,column=10)
tk.Button(ObjectFrame, text="<", command=ObjectIDSub, state="disabled").grid(row=30, column=5)
tk.Button(ObjectFrame, text="Zvolit", command=ObjectIDSelect, state="disabled").grid(row=30, column=10)
tk.Button(ObjectFrame, text=">", command=ObjectIDAdd, state="disabled").grid(row=30, column=15)
tk.Checkbutton(ObjectFrame, text="Ořiznutí", variable=TkCrop, onvalue=True, offvalue=False).grid(row=40, column=10)
tk.Checkbutton(FolderFrame, text="Vyskyt Mionů", variable=TKMuons, onvalue=True, offvalue=False).grid(row=40, column=10, sticky="n")

#InfoFrames
FolderInfoFrame=tk.LabelFrame(root,text="Analýza složky", pady=5, padx=5)
FolderInfoFrame.grid(row=10, column=20)
FileInfoFrame=tk.LabelFrame(root,text="Analýza souboru", pady=5, padx=5)
FileInfoFrame.grid(row=20, column=20)
ObjectInfoFrame=tk.LabelFrame(root, text="Objekt", pady=5, padx=5)
ObjectInfoFrame.grid(row=30,column=20)

#Folders
RefreshObjectFrame()
RefreshFileFrame()
RefreshFolderInfoFrame()
RefreshObjectInfoFrame()
RefreshFileInfoFrame()

#Objects
def HistFileEnergyAlpha():
    global Detections
    PlotMaps.HistogrameFunction(1,1,Detections,TkLOG.get(),TkBins.get())
    
def HistFileEnergyBeta():
    global Detections
    PlotMaps.HistogrameFunction(2,1,Detections,TkLOG.get(),TkBins.get())
    
def HistFileEnergyGama():
    global Detections
    PlotMaps.HistogrameFunction(3,1,Detections,TkLOG.get(),TkBins.get())
    
def HistFileEnergyMuon():
    global Detections
    PlotMaps.HistogrameFunction(4,1,Detections,TkLOG.get(),TkBins.get())
    
def HistFileEnergyHEP():
    global Detections
    PlotMaps.HistogrameFunction(5,1,Detections,TkLOG.get(),TkBins.get())

def HistTypeDistributionFile():
    global Detections
    PlotMaps.HistogrameDistFile(Detections)
    
def HistEnergyAllFile():
    global Detections
    PlotMaps.HistogramAllFile(1,Detections,TkLOG.get(),TkBins.get())
    
def HistPixAllFile():
    global Detections
    PlotMaps.HistogramAllFile(2,Detections,TkLOG.get(),TkBins.get()) 
    
def HistFolderEnergyAlpha():
    global AllDetections
    PlotMaps.HistogrameFunction(1,1,AllDetections,TkLOG.get(),TkBins.get())
    
def HistFolderEnergyBeta():
    global AllDetections
    PlotMaps.HistogrameFunction(2,1,AllDetections,TkLOG.get(),TkBins.get())
    
def HistFolderEnergyGama():
    global AllDetections
    PlotMaps.HistogrameFunction(3,1,AllDetections,TkLOG.get(),TkBins.get())
    
def HistFolderEnergyMuon():
    global AllDetections
    PlotMaps.HistogrameFunction(4,1,AllDetections,TkLOG.get(),TkBins.get())
    
def HistFolderEnergyHEP():
    global AllDetections
    PlotMaps.HistogrameFunction(5,1,AllDetections,TkLOG.get(),TkBins.get())

def HistTypeDistributionFolder():
    global AllDetections
    PlotMaps.HistogrameDistFile(AllDetections)
    
def HistEnergyAllFolder():
    global AllDetections
    PlotMaps.HistogramAllFile(1,AllDetections,TkLOG.get(),TkBins.get())
    
def HistPixAllFolder():
    global AllDetections
    PlotMaps.HistogramAllFile(2,AllDetections,TkLOG.get(),TkBins.get())   
    
def Bin():
    TkBins.set(TkBin.get())

#Graphs
GraphPlotFrame=tk.LabelFrame(root,text="Histogramy", pady=5, padx=5)
GraphPlotFrame.grid(row=10, column=30)
TkBin=tk.Entry(GraphPlotFrame)
TkBin.insert(20, "Počet Binů")
TkBin.grid(row=7,column=10,sticky="w")
tk.Button(GraphPlotFrame, command=Bin, text="Potvrdit").grid(row=9,column=10,sticky="w")
GraphPlotFrameFolder=tk.LabelFrame(GraphPlotFrame, text="Složka", pady=5,padx=5)
GraphPlotFrameFolder.grid(row=10,column=10)

tk.Checkbutton(GraphPlotFrame, text="Log měřítko", variable=TkLOG, onvalue=True, offvalue=False).grid(row=5, column=10,sticky="w")
tk.Button(GraphPlotFrameFolder, command=HistEnergyAllFolder, text="energii", state='disabled').grid(row=10,column=10)
tk.Button(GraphPlotFrameFolder, command=HistPixAllFolder, text="velikosti", state='disabled').grid(row=20,column=10)
tk.Button(GraphPlotFrameFolder, command=HistTypeDistributionFolder, text="zastoupeni typu", state='disabled').grid(row=30,column=10)
tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyAlpha, text="energii alfa", state='disabled').grid(row=40,column=10)
tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyBeta, text="energii beta", state='disabled').grid(row=50,column=10)
tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyGama, text="energii gama", state='disabled').grid(row=60,column=10)
tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyMuon, text="energii mionu", state='disabled').grid(row=70,column=10)
tk.Button(GraphPlotFrameFolder, command=HistFolderEnergyHEP, text="energii HEP", state='disabled').grid(row=80,column=10)

GraphPlotFrameFile=tk.LabelFrame(GraphPlotFrame, text="Soubor", pady=5,padx=5)
GraphPlotFrameFile.grid(row=10,column=20)
tk.Button(GraphPlotFrameFile, command=HistEnergyAllFile, text="energii", state='disabled').grid(row=10,column=10)
tk.Button(GraphPlotFrameFile, command=HistPixAllFile, text="velikosti", state='disabled').grid(row=20,column=10)
tk.Button(GraphPlotFrameFile, command=HistTypeDistributionFile, text="zastoupeni typu", state='disabled').grid(row=30,column=10)
tk.Button(GraphPlotFrameFile, command=HistFileEnergyAlpha, text="energii alfa", state='disabled').grid(row=40,column=10)
tk.Button(GraphPlotFrameFile, command=HistFileEnergyBeta, text="energii beta", state='disabled').grid(row=50,column=10)
tk.Button(GraphPlotFrameFile, command=HistFileEnergyGama, text="energii gama", state='disabled').grid(row=60,column=10)
tk.Button(GraphPlotFrameFile, command=HistFileEnergyMuon, text="energii mionu", state='disabled').grid(row=70,column=10)
tk.Button(GraphPlotFrameFile, command=HistFileEnergyHEP, text="energii HEP", state='disabled').grid(row=80,column=10)

def ShowSingle(ID):
    global Detections
    Array=DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1])
    Objects=DataOperations.SeparateObjects(Array)
    Plot=DataOperations.MakeArraySingleCategory(Array,Objects, Detections, ID)
    PlotMaps.MakePlotFromArray(Plot, False)

def ShowAlpha():
    ShowSingle(1)
    
def ShowBeta():
    ShowSingle(2)
    
def ShowGama():
    ShowSingle(3)
    
def ShowMuon():
    ShowSingle(4)
    
def ShowHEP():
    ShowSingle(5)

ObjectSelectFrame=tk.LabelFrame(root, text="Zobrazit pouze", pady=5,padx=5)
ObjectSelectFrame.grid(row=20,column=30)
tk.Button(ObjectSelectFrame,command=ShowAlpha, text="alfa", state="disabled").grid(row=10,column=10,sticky="nsew")
tk.Button(ObjectSelectFrame,command=ShowBeta, text="beta", state="disabled").grid(row=20,column=10,sticky="nsew")
tk.Button(ObjectSelectFrame,command=ShowGama, text="gama", state="disabled").grid(row=30,column=10,sticky="nsew")
tk.Button(ObjectSelectFrame,command=ShowMuon, text="miony", state="disabled").grid(row=40,column=10,sticky="nsew")
tk.Button(ObjectSelectFrame,command=ShowHEP, text="HEP", state="disabled").grid(row=50,column=10,sticky="nsew")

if os.path.isfile('config.txt'):
    TkFolderPath.set(InputsOutputs.LoadConfigPath())
    ListOfFiles=InputsOutputs.LoadFolder(InputsOutputs.LoadConfigPath())
    TkFileMaxIndex.set(len(ListOfFiles))
    RefreshFolderFrame()
    RefreshFileFrame()

CutRot=tk.IntVar()
YCut=tk.IntVar()
YCMin=tk.IntVar()
YCMax=tk.IntVar()
HWidth=tk.IntVar()

def CutRefresh():
    tk.Label(HCutting, text="poloha = " +str(YCut.get())).grid(row=10, column=20)
    tk.Label(HCutting, text="šířka = " + str(HWidth.get())).grid(row=15, column=20)

def HCutD10():
    YCut.set(YCut.get()-10)
    CutRefresh()
    
def HCutD():
    YCut.set(YCut.get()-1)
    CutRefresh()
    
def HCutU():
    YCut.set(YCut.get()+1)
    CutRefresh()
    
def HCutU10():
    YCut.set(YCut.get()+10)
    CutRefresh()
    
def CutRotU():
    CutRot.set(CutRot.get()+15)
    if CutRot.get()>360:
        CutRot.set(CutRot.get()-360)
    if CutRot.get()<0:
        CutRot.set(CutRot.get()+360)
    tk.Label(TkRotation, text="Úhel natočení="+str(CutRot.get())+" °").grid(row=40, column=20)
    
def CutRotD():
    CutRot.set(CutRot.get()-15)
    if CutRot.get()>360:
        CutRot.set(CutRot.get()-360)
    if CutRot.get()<0:
        CutRot.set(CutRot.get()+360)
    tk.Label(TkRotation, text="Úhel natočení="+str(CutRot.get())+" °").grid(row=40, column=20)
    
def HWidthU():
    HWidth.set(HWidth.get()+1)
    CutRefresh()
    
def HWidthD():
    if HWidth.get()>0:
        HWidth.set(HWidth.get()-1)
    CutRefresh()
    
def ShowHLine():
    Array=interpolation.rotate(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]),angle=CutRot.get())
    PlotMaps.PlotArray(Array, YCut.get(),(YCut.get()+HWidth.get()))

def MakeHCut():
    Array=interpolation.rotate(DataOperations.MakeArrayFromFile(TkFolderPath.get(),ListOfFiles[TkFileIndex.get()-1]),angle=CutRot.get())
    PlotMaps.ShowHCut(Array, YCut.get(), HWidth.get())    

Cutting=tk.LabelFrame(root, text="Řez", padx=5, pady=5)
Cutting.grid(row=10, column=60, sticky="N")
HCutting=tk.LabelFrame(Cutting, text="Oblast řezu", padx=5, pady=5)
HCutting.grid(row=10, column=10)
tk.Label(HCutting, text="Poloha = " +str(YCut.get())).grid(row=10, column=20)
tk.Label(HCutting, text="Šířka = " + str(HWidth.get())).grid(row=15, column=20)
tk.Button(HCutting, text="↓↓", command=HCutD10).grid(row=10, column=10)
tk.Button(HCutting, text="↓", command=HCutD).grid(row=10, column=15)
tk.Button(HCutting, text="↑", command=HCutU).grid(row=10, column=25)
tk.Button(HCutting, text="↑↑", command=HCutU10).grid(row=10, column=30)
tk.Button(HCutting, text="Rozšířit", command=HWidthU).grid(row=20, column=25)
tk.Button(HCutting, text="Zúžit", command=HWidthD).grid(row=20, column=15)
tk.Button(Cutting, text="Zobraz oblast řezu", command=ShowHLine).grid(row=20, column=10)

TkRotation=tk.LabelFrame(Cutting, text="rotace")
TkRotation.grid(row=10, column=15)
tk.Button(TkRotation, text="↻", command=CutRotU).grid(row=30, column=15)
tk.Button(TkRotation, text="↺", command=CutRotD).grid(row=30, column=25)
tk.Label(TkRotation, text="Úhel natočení="+str(CutRot.get())+" °").grid(row=40, column=20)
tk.Button(Cutting, text="Proveď řez", command=MakeHCut).grid(row=50, column=10)

root.mainloop()