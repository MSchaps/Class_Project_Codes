#This script holds a module that selects out parcels from the original feature classed based on the values in the created Homestead_YN and Rental
#fields
def Parcel_Selector(workspace, Final_Path, GDB_Name):
    import arcpy
    from arcpy import env
    env.workspace = workspace
    env.overwriteOutput = True
    #Creates the Geodatabase to hold the final output
    arcpy.CreateFileGDB_management(Final_Path, GDB_Name)
    #Creates a path to the new created geodatabase to be used later
    Geodatabase = Final_Path + "\\" + GDB_Name
    #Creates a list of the feature classes in the original geodatabase
    fclist = arcpy.ListFeatureClasses("*", '')
    for fc in fclist:
        print fc
        #Creates a path for the new feature classes that are created from the selected parcels
        new_feature_path = Geodatabase + r'\\{0}'.format(fc)
        #Selection statement that selects parcels if the Rental Field is Yes or Maybe
        where = '''"RENTAL" in ('Y', 'M')'''
        #Selection statement that selects parcels if the Homestead_YN field is Yes or Maybe
        where2 = '''"HOMESTEAD_YN" in ('Y', 'M')'''
        #Creates feature layer to be selected
        arcpy.MakeFeatureLayer_management(fc, "{0}".format(fc))
        #Selection that selects the values based on the rental selection statement
        arcpy.SelectLayerByAttribute_management("{0}".format(fc), "NEW_SELECTION", where)
        #Adds the parcels that are selected with the homestead YN to the original selection
        arcpy.SelectLayerByAttribute_management("{0}".format(fc), "ADD_TO_SELECTION", where2)
        #Copies the selected features, and outputs the saved feature class to the new final geodatabase
        arcpy.CopyFeatures_management("{0}".format(fc), new_feature_path)

