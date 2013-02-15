# Name: TestModelRadialLineOfSight.py
# Description: Automatic Test of Radial Line Of Sight Model
# Requirements: ArcGIS Desktop Standard with Spatial Analyst Extension

import arcpy
import os
import sys
import traceback

import TestUtilities

def RunTest():
    try:
        arcpy.AddMessage("Starting Test: TestModelRadialLineOfSight")
        
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            # Raise a custom exception
            raise Exception("LicenseError")        
        
        # WORKAROUND
        print "Creating New Scratch Workspace (Workaround)"    
        TestUtilities.createScratch()
            
        # Verify the expected configuration exists
        inputPointsFC =  os.path.join(TestUtilities.inputGDB, "RlosObserverWebMerc")
        inputSurface =  os.path.join(TestUtilities.defaultGDB, "Jbad_SRTM_USGS_EROS")
        outputVizFC =  os.path.join(TestUtilities.outputGDB, "RlosVizOutput") 
        toolbox = TestUtilities.toolbox
        
        # Check For Valid Input
        objects2Check = []
        objects2Check.extend([inputPointsFC, inputSurface, toolbox])
        for object2Check in objects2Check :
            desc = arcpy.Describe(object2Check)
            if desc == None :
                raise Exception("Bad Input")
            else :
                print "Valid Object: " + desc.Name 
        
        # Set environment settings
        print "Running from: " + str(TestUtilities.currentPath)
        print "Geodatbase path: " + str(TestUtilities.geodatabasePath)
        
        arcpy.env.overwriteOutput = True
        arcpy.env.scratchWorkspace = TestUtilities.scratchGDB
        arcpy.ImportToolbox(toolbox, "VandRAlias")
    
        inputFeatureCount = int(arcpy.GetCount_management(inputPointsFC).getOutput(0)) 
        print "Input FeatureClass: " + str(inputPointsFC)
        print "Input Feature Count: " +  str(inputFeatureCount)
            
        if (inputFeatureCount < 1) :
            print "Invalid Input Feature Count: " +  str(inputFeatureCount)
                       
        forceVisibilityToInfinity = False
           
        ########################################################3
        # Execute the Model under test:   
        arcpy.RadialLineOfSight_VandRAlias(inputPointsFC, inputSurface, outputVizFC, forceVisibilityToInfinity)
        ########################################################3
    
        # Verify the results    
        outputFeatureCountViz = int(arcpy.GetCount_management(outputVizFC).getOutput(0)) 
        print "Output FeatureClass: " + str(outputVizFC)
        print "Output Feature Count: " +  str(outputFeatureCountViz)
                 
        if (outputFeatureCountViz < 1) :
            print "Invalid Output Feature Count: " + str(outputFeatureCountViz)
            raise Exception("Test Failed")
            
        # WORKAROUND: delete scratch db
        print "Deleting Scratch Workspace (Workaround)"    
        TestUtilities.deleteScratch()        
        
        print "Test Successful"
                
    except arcpy.ExecuteError: 
        # Get the tool error messages 
        msgs = arcpy.GetMessages() 
        arcpy.AddError(msgs) 
    
        # return a system error code
        sys.exit(-1)
        
    except Exception as e:
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"
    
        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)
    
        # return a system error code
        sys.exit(-1)
        
    finally:
        # Check in the 3D Analyst extension
        arcpy.CheckInExtension("Spatial")        
        

RunTest()