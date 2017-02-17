#This script holds a module that deletes all of the fields from the new feature classes besides the Homestead YN field and the Rental field. This
#is mainly because of agreements I have made with certain counties to do so.
def Field_Deleter(final_workspace):
    import arcpy
    from arcpy import env
    env.workspace = final_workspace
    env.overwriteOutput = True
    fclist = arcpy.ListFeatureClasses("*", '')
    for fc in fclist:
        print fc
        Feature = final_workspace + "\\" + fc
        fieldlist = arcpy.ListFields(Feature)
        fields = [f.name for f in fieldlist]
        for field in fields:
            #a field is not the Rental, Homestead_YN field, or one of the undeleteable fields
            if field not in ("RENTAL", "HOMESTEAD_YN", "OBJECTID", "Shape", "Shape_Length", "Shape_Area", "OBJECTID_1", "OBJECTID_12"):
                #The field is deleted
                arcpy.DeleteField_management(fc, field)

