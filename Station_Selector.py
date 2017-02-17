def Station_Selector(workspace, Feature_Class):
    import arcpy
    from arcpy import env
    env.workspace = workspace
    env.overwriteOutput = True
    target_fc = workspace + r'\\' + Feature_Class
    fieldlist = arcpy.ListFields(target_fc)
    fieldnames = [field.name for field in fieldlist]
    arcpy.MakeFeatureLayer_management(target_fc, 'Transit_Stops')
    fieldnames.remove('OBJECTID')
    fieldnames.remove('Shape')
    fieldnames.remove('site_id')
    fieldnames.remove('geonodenam')
    for fn in fieldnames:
        route_name = fn.strip('R_').strip('_YN')
        print 'Stations that have the route ' + str(route_name) + ' are being parsed'
        where = "{0} = 'Y'".format(fn)
        arcpy.SelectLayerByAttribute_management('Transit_Stops', 'NEW_SELECTION', where)
        arcpy.CopyFeatures_management('Transit_Stops', 'Route_' + route_name)
workspace = r'C:\\GIS\\Cyber_GIS\\Final_Project\\Geodatabase\\Workspace.gdb'
Feature_Class = r'TransitStopsGPS'
Station_Selector(workspace, Feature_Class)