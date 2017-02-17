def Merger(workspace):
    import arcpy
    import re
    import os
    import sys
    import unicodedata
    from arcpy import env
    env.workspace = workspace
    env.overwriteOutput = True
    fclist = arcpy.ListFeatureClasses("*", '')
    for fc in fclist:
        print fc
        Feature = workspace + "\\" + fc
        fieldlist = arcpy.ListFields(Feature)
        fields = [f.name for f in fieldlist]
        for field in fieldlist: