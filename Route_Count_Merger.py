def Route_Count_Merger(workspace, Feature_Class):
    import arcpy
    from arcpy import env
    env.workspace = workspace
    env.overwriteOutputs = True
    route_fc = r'C:\\GIS\\Cyber_GIS\\Final_Project\\Geodatabase\\Workspace.gdb\\TransitRoutes'
    Count_fc = workspace + r'\\' + Feature_Class
    arcpy.MakeFeatureLayer_management(route_fc, "Routes")
    arcpy.MakeFeatureLayer_management(Count_fc, 'Counts')
    arcpy.AddField_management('Counts', 'Route_Num', 'TEXT', '', '', '5', 'Route_Num')
    route_cursor = arcpy.da.SearchCursor("Routes", "route")
    for row in route_cursor:
        route = row[0]
        print "Route " + str(route) + ' is being joined to counts'
        where = "Route = '{0}'".format(route)
        arcpy.SelectLayerByAttribute_management('Routes', 'NEW_SELECTION', where)
        arcpy.SelectLayerByLocation_management('Counts', 'HAVE_THEIR_CENTER_IN', 'Routes', '', 'NEW_SELECTION')
        arcpy.CalculateField_management('Counts', 'Route_Num', '{0}'.format(route), "PYTHON_9.3")
        arcpy.SelectLayerByAttribute_management('Counts', 'CLEAR_SELECTION')
    arcpy.CopyFeatures_management('Counts', 'Counts_with_Routes')
    arcpy.Dissolve_management(workspace + r'\\' + 'Counts_with_Routes', 'Route_Counts_Dissolved', "Route_Num", statistics_fields=[['EAM_COUNT','SUM'],['AMP_COUNT','SUM'],['MID_COUNT','SUM'],['PMP_COUNT', 'SUM'], ['EVE_COUNT', 'SUM'], ['NIGHT_COUN', 'SUM'], ['OWL_COUNT', 'SUM'], ['TOTAL_COUN', 'SUM']])
workspace = r'C:\\GIS\\Cyber_GIS\\Final_Project\\Geodatabase\\Workspace.gdb'
Feature_Class = r'TransitCountHeadwaySummary'
Route_Count_Merger(workspace, Feature_Class)