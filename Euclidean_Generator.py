#This script generates the euclidean distance analyses from the business layers.
def Eudlidean_Generator(business_workspace, final_workspace):
    import arcpy
    from arcpy import env
    env.workspace = business_workspace
    env.overwriteOutput = True
    #Checks out the Spatial Analysis extension
    arcpy.CheckOutExtension("Spatial")
    fclist = arcpy.ListFeatureClasses("*", '')
    for fc in fclist:
        print fc
        #Creates a name/path for the new euclidean distance rasters
        OutEuc = final_workspace + "\\" + fc + "_EucDist"
        #Creates Euclidean Distance Rasters with a maximum extent of 100000 meters, and 10 meter cells
        OutEucDist = arcpy.sa.EucDistance(fc, 100000, 10)
        #Saves the Euclidean Distance raster
        OutEucDist.save(OutEuc)
        Output_direction_raster = ""
        #Creates a temporary raster environment
        tempEnvironment0 = arcpy.env.snapRaster
        arcpy.env.snapRaster = ""
        tempEnvironment1 = arcpy.env.extent
        #Sets the temporary raster extent for the euclidean distance analyses to the extent of the 7 county metro. This is important
        #becasue otherwise, I have noticed that if there are no more additional features in a certain direction of another feature, the
        #Euclidean analysis will be cropped in that direction
        arcpy.env.extent = "419967.47231056 4924223.79121654 521254.699796891 5029129.99272224"
        arcpy.gp.EucDistance_sa(fc, OutEuc, "", 10)
        arcpy.env.snapRaster = tempEnvironment0
        arcpy.env.extent = tempEnvironment1

