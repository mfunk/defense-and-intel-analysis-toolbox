'''
@author: cmoore
'''
import arcpy
import os
import sys

currentPath = os.path.dirname(__file__)
geodatabasePath = os.path.normpath(os.path.join(currentPath, r"../../../data/geodatabases/"))
csvPath = os.path.normpath(os.path.join(currentPath, r"../../../data/csv/"))
dbfPath = os.path.normpath(os.path.join(currentPath, r"../../../data/dbf/"))

scratchPath = geodatabasePath
toolboxesPath = os.path.normpath(os.path.join(currentPath, r"../../../toolboxes/"))                

inputGDB  = os.path.join(geodatabasePath, "test_inputs.gdb")
outputGDB = os.path.join(geodatabasePath, "test_outputs.gdb")
defaultGDB = os.path.join(geodatabasePath, "default.gdb")
scratchGDB = os.path.join(scratchPath, "scratch.gdb")

toolbox = os.path.join(toolboxesPath, "Position Analysis Tools.tbx")

def createScratch() :
    try :
        arcpy.CreateFileGDB_management(scratchPath, "scratch")                                          
    except:    
        print "scratch.gdb already exists"
        
    return

def deleteScratch() :
    try :   
        arcpy.Delete_management(scratchGDB)
    except:    
        print "scratch.gdb delete failed"
        
    return    
