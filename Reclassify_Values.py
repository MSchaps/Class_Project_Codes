def Value_Reclassify(final_workspace):
    import arcpy
    from arcpy import env
    env.workspace = final_workspace
    env.overwriteOutput = True
    fclist = arcpy.ListFeatureClasses(feature_type="Polygon")
    print fclist
    for fc in fclist:
        if fc.endswith("_Join"):
            arcpy.AddField_management(fc, "Final_Score", "TEXT", "", "" , "", "Final_Score")
            cursor_fields = ("Grocery_Stores_EucDist", "Gas_Stations_EucDist", "Fast_Food_EucDist", "Farmers_Markets_EucDist", "Final_Score")
            cursor = arcpy.da.UpdateCursor(fc, cursor_fields)
            for row in cursor:
                groc_dist = row[0]
                gas_dist = row[1]
                fast_dist = row[2]
                farm_dist = row[3]
                if groc_dist < fast_dist and groc_dist < gas_dist:
                    row[4] = "3"
                    cursor.updateRow(row)
                elif farm_dist < fast_dist and farm_dist < gas_dist:
                    row[4] = "3"
                    cursor.updateRow(row)
                elif fast_dist < groc_dist and fast_dist < farm_dist:
                    row[4] = "1"
                    cursor.updateRow(row)
                elif gas_dist < groc_dist and gas_dist < farm_dist:
                    row[4] = "1"
                    cursor.updateRow(row)
                elif farm_dist < fast_dist and farm_dist > gas_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif farm_dist < gas_dist and farm_dist > fast_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif groc_dist < fast_dist and groc_dist > gas_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif groc_dist < gas_dist and groc_dist > fast_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif fast_dist < groc_dist and fast_dist > farm_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif fast_dist < farm_dist and fast_dist > groc_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif gas_dist < groc_dist and gas_dist > farm_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
                elif gas_dist < farm_dist and gas_dist > groc_dist:
                    row[4] = "2"
                    cursor.updateRow(row)
