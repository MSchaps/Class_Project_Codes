#This script holds the module that goes through all of the feature classes in a geodatabase, and reporjects them to NAD 1983 Zone 15 N.
def ReprojectData(workspace):
    #Import the needed modules
    import arcpy
    import unicodedata
    #Import the environment variable from the arcpy module
    from arcpy import env
    #Sets the workspace to the geodatabase that contains the original parcels
    arcpy.env.workspace = workspace
    #Sets Overwrite outputs setting to true
    arcpy.env.OverwriteOutputs = True
    #Createas a list of all of the feature classes in the geodatabase
    fclist = arcpy.ListFeatureClasses("*","")
    for fc in fclist:
        #Creates a variable to contain the description information of the feature classes
        desc = arcpy.Describe(fc)
        #Sets a variable to contain the spatial reference of each feature class
        SR = desc.spatialReference
        #Creates a variable to contains the name of the spatial reference for each feature class
        InProj = SR.name
        #If the projection of the feature class is already NAD 1983 Zone 15 N, it is skipped
        if InProj == "NAD_1983_UTM_Zone_15N":
            print fc + " projection is already UTM Zone 15 N"
            pass
        else:
            #Creates a variable for the name of the feature class
            fc_string = unicodedata.normalize('NFKD', fc).encode('ascii','ignore')
            #Splits the name of a feature class, and its extension
            fc_name = fc_string.split(".shp")[0]
            InData = fc
            print InData + " currently has the projection of " + SR.name
            #Sets the name of the output data after it is reporjected
            OutData = workspace + '\\' + fc_name + "_UTM_Zone_15_N"
            print fc + " is being reprojectd to NAD 1983 UTM Zone 15 N"
            #Projects the data to the correct projection
            arcpy.Project_management(InData,OutData,"26915","")
            print fc + " Has been reprojected to NAD 1983 UTM Zone 15 N, and can be found in " + workspace
            print "Deleting original Parcel Feature"
            #Deletes the non projected feature classes to save space
            arcpy.Delete_management(fc)
            print fc + " has been deleted"
