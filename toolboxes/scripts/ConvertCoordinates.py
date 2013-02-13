# ---------------------------------------------------------------------------
# ConvertCoordinates.py
# Usage: ConvertCoordinates <Input_Table> <Input_Coordinate_Format> <X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_> <Y_Field__Latitude_> <Output_Table> <Spatial_Reference> 
# Description: 
# Converts coordinates in a table between Decimal Degrees (DD), Degrees Decimal Minutes (DDM), Degrees Minutes Seconds (DMS), Universal Transverse Mercator (UTM), Military Grid Reference System (MGRS), US National Grid (USNG), Global Area Reference System (GARS) and Geographic Reference (GeoRef).
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy, sys, os
from arcpy import env

# Load required toolboxes
scriptpath = sys.path[0]
toolboxpath = os.path.join(scriptpath,"..\\Toolbox.tbx")
arcpy.ImportToolbox(toolboxpath) #("C:\\Work\\TOS\\Intel\\Toolbox.tbx")

# Script arguments
Input_Table = arcpy.GetParameterAsText(0)
arcpy.AddMessage(Input_Table)
if Input_Table == '#' or not Input_Table:
    Input_Table = "C:\\Workspace\\Data\\Geometry Importers\\linewizard.dbf" # provide a default value if unspecified

Input_Coordinate_Format = arcpy.GetParameterAsText(1)
if Input_Coordinate_Format == '#' or not Input_Coordinate_Format:
    Input_Coordinate_Format = "DD" # provide a default value if unspecified

X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_ = arcpy.GetParameterAsText(2)
if X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_ == '#' or not X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_:
    X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_ = "Lond" # provide a default value if unspecified

Y_Field__Latitude_ = arcpy.GetParameterAsText(3)
if Y_Field__Latitude_ == '#' or not Y_Field__Latitude_:
    Y_Field__Latitude_ = "Latd" # provide a default value if unspecified

Output_Table = arcpy.GetParameterAsText(4)
arcpy.AddMessage(Output_Table)
if Output_Table == '#' or not Output_Table:
    Output_Table = "C:\\Workspace\\ArcGIS Defense 10.1\\Intel Table Template\\Maps\\default.gdb\\OutputTable" # provide a default value if unspecified

Spatial_Reference = arcpy.GetParameterAsText(5)
if Spatial_Reference == '#' or not Spatial_Reference:
    Spatial_Reference = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision" # provide a default value if unspecified


# Construct a pathname to write scratch data.  In this example, the pathname should 
# be a folder, not a geodatabase. Start by getting the scratch workspace environment
# from geoprocessing. If the environment is a folder (type = "FileSystem"), use it.
# Otherwise, use the system TEMP folder.
scratchWS = env.scratchWorkspace

scratchTable = os.path.join(scratchWS,"cc_temp")
#arcpy.CopyRows_management(Input_Table, scratchWS, "")

# Local variables:
intermed = Output_Table

# Process: Copy Rows
arcpy.CopyRows_management(Input_Table, Output_Table, "")

# Process: Add Unique Row ID
#arcpy.gp.toolbox = "C:/Workspace/ArcGIS Defense 10.1/Intel Table Template/Maps/Toolboxes/Toolbox.tbx";
# Warning: the toolbox C:/Workspace/ArcGIS Defense 10.1/Intel Table Template/Maps/Toolboxes/Toolbox.tbx DOES NOT have an alias. 
# Please assign this toolbox an alias to avoid tool name collisions
# And replace arcpy.gp.AddUniqueRowID(...) with arcpy.AddUniqueRowID_ALIAS(...)
arcpy.gp.AddUniqueRowID(Output_Table, "JoinID")

# Process: Convert Coordinate Notation (GARS)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "GARS", "JoinID", Spatial_Reference)

# Process: Join GARS To Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "GARS")

# Process: Convert Coordinate Notation (DD)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "DD", "JoinID", Spatial_Reference)

# Process: Join DD To Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "DDLat;DDLon")

# Process: Convert Coordinate Notation (DDM)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "DDM", "JoinID", Spatial_Reference)

# Process: Join DDM to Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "DDMLat;DDMLon")

# Process: Convert Coordinate Notation (DMS)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "DMS", "JoinID", Spatial_Reference)

# Process: Join DMS To Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "DMS")

# Process: Convert Coordinate Notation (UTM)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "UTM", "JoinID", Spatial_Reference)

# Process: Join UTM To Coords
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "UTM")

# Process: Convert Coordinate Notation (MGRS)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "MGRS", "JoinID", Spatial_Reference)

# Process: Join MGRS To Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "MGRS")

# Process: Convert Coordinate Notation (USNG)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "USNG", "JoinID", Spatial_Reference)

# Process: Join USNG To Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "USNG")

# Process: Convert Coordinate Notation (GeoRef)
arcpy.ConvertCoordinateNotation_management(intermed, scratchTable, X_Field__Longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__Latitude_, Input_Coordinate_Format, "GEOREF", "JoinID", Spatial_Reference)

# Process: Join GeoRef To Table
arcpy.JoinField_management(intermed, "JoinID", scratchTable, "JoinID", "GEOREF")

