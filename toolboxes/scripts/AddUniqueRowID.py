
# Adds a new field of unique row numbers to a table

import os, sys, traceback
import arcpy

dataset = arcpy.GetParameterAsText(0)
fieldName = arcpy.GetParameterAsText(1)

counter = 1

try:
    
    # add unique ID field
    arcpy.AddMessage("Adding field " + str(fieldName))
    arcpy.AddField_management(dataset,fieldName,"LONG")

    # add unique numbers to each row
    arcpy.AddMessage("Adding unique row IDs")
    rows = arcpy.UpdateCursor(dataset)
    for row in rows:
        row.setValue(fieldName,counter)
        rows.updateRow(row)
        counter += 1
    del row
    del rows
    
    # set output
    arcpy.SetParameter(0,dataset)
    

except arcpy.ExecuteError:
    error = True
    # Get the tool error messages 
    msgs = arcpy.GetMessages() 
    arcpy.AddError(msgs) 
    print msgs

except:
    # Get the traceback object
    error = True
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

    # Return python error messages for use in script tool or Python Window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)

    # Print Python error messages for use in Python / Python Window
    print pymsg + "\n"
    print msgs