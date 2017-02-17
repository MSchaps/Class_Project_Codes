#This script holds a module that joins the values of the rasters to the parcels
def Value_Joiner(final_workspace):
    import arcpy
    from arcpy import env
    env.workspace = final_workspace
    env.overwriteOutput = True
    #Checks out the Spatial Analysis Extension
    arcpy.CheckOutExtension("Spatial")
    #Lists feature classes in the Geodatabase that are polygons. THis is important becasue the geodatabase now also contains rasters
    fclist = arcpy.ListFeatureClasses(feature_type="Polygon")
    print fclist
    for fc in fclist:
        print fc
        #Creates Centroids for each of the polygon parcel feature classes. This is important for the later join. These centroid feature classes
        #are added to the final geodatabase
        centroids = final_workspace + "\\" + fc + "_Points"
        arcpy.FeatureToPoint_management(fc, centroids)
    #Creates a list of all of the raster files in the final geodatabase
    Raster_list = arcpy.ListRasters("*", "")
    #Creates a list of all of the point feature classes in the Geodatabase
    Ponint_list = arcpy.ListFeatureClasses(feature_type="Point")
    for point in Ponint_list:
        print point
        #Creates a list of all of the rasters that will be used in the join, and what the name of the field in the later join will be
        inRasterList = [[Raster_list[0], str(Raster_list[0])], [Raster_list[1], str(Raster_list[1])],
                        [Raster_list[2], str(Raster_list[2])], [Raster_list[3], str(Raster_list[3])]]
        #Joins all of the rasters to the point feature classes
        arcpy.sa.ExtractMultiValuesToPoints(point, inRasterList, "NONE")
    for fc in fclist:
        #Takes the joined points, and spatially joins them to the rental and homestead rasters, and then adds the new joined parcels feature
        #classes to the final geodatabase
        arcpy.SpatialJoin_analysis(fc, fc + "_Points",fc + "_Join", "", "", "", "COMPLETELY_CONTAINS")
    print Raster_list
    print Ponint_list


