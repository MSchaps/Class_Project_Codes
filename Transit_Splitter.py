def Transit_Route_Adder(workspace, table, feature_class):
    import arcpy
    from arcpy import env
    env.workspace = workspace
    env.overwriteOutput = True
    transit_points = workspace + r'\\' + feature_class
    route_table = workspace + r'\\' + table
    tablefields = ("site_id", "Route")
    fieldlist = arcpy.ListFields(transit_points)
    fieldnames = [f.name for f in fieldlist]
    stop_searcher = arcpy.da.SearchCursor(route_table, tablefields)
    route_searcher = arcpy.da.SearchCursor(route_table, tablefields)
    route_cursor = arcpy.da.SearchCursor(route_table, tablefields)
    mostroutes = 0
    stoplist = []
    uniqueroutelist = []
    for row in stop_searcher:
        stop = row[0]
        route = row[1]
        if stop not in stoplist:
            stoplist.append(stop)
    pairs = []
    for row in route_searcher:
        route = row[1]
        if route not in uniqueroutelist:
            uniqueroutelist.append(route)
    print "The total number of unique routes is " + str(len(uniqueroutelist))
    for ur in uniqueroutelist:
        arcpy.AddField_management(transit_points, "R_" + str(ur) + "_YN", "TEXT")
    for row in route_cursor:
        stoproute = ([])
        cstop = row[0]
        route = row[1]
        pair = [cstop,route]
        pairs.append(pair)
    for st in stoplist:
        routelist = []
        for p in pairs:
            if st == p[0]:
                print p[0]
                if p[1] not in routelist:
                    routelist.append(p[1])
        print routelist
        numroutes = len(routelist)
        print numroutes
        if numroutes > mostroutes:
            mostroutes = numroutes
    print mostroutes
    for fieldname in fieldnames:
        fields = ("site_id", fieldname)
        valuecursor = arcpy.da.UpdateCursor(transit_points, fields)
        for row in valuecursor:
            currentstop = row[0]
            print "Station being parsed is " + str(currentstop)
            for p in pairs:
                if p[0] == currentstop:
                    print "Pair Station Match Found with " + str(p[0])
                    print fieldname
                    print "R_" + str(p[1]) + "_YN"
                    if "R_" + str(p[1]) + "_YN" == fieldname:
                        print "Match found with route " + str(p[1])
                        row[1] =+ 'Y'
                        valuecursor.updateRow(row)
workspace = r'C:\\GIS\\Cyber_GIS\\Final_Project\\Geodatabase\\Workspace.gdb'
table = r'STOP_RouteListByStop'
feature_class = r'TransitStopsGPS'
Transit_Route_Adder(workspace, table, feature_class)

