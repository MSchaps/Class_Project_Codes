#This script contains a module that loops through all of the values of the fields, and populates a new field with values based on these original
#values.
def FieldTypeChanger(workspace):
    import arcpy
    from arcpy import env
    env.workspace = workspace
    env.overwriteOutput = True
    #Sets values to look through for in the original homestead fields to set the values in the new field to "Y"
    Homestead_Yes = ("Relative Homestead", "Owner/Relative Homestead", "Owner Homestead", "Y", "FULL HOMESTEAD", "2AHGA-Agricultural Homestead - HGA", \
                     "1BREM-Blind/Disabled Homestead Ag Remainder", "1BNA-Blind/Disabled Homestead Non Ag", "1A-Residential Homestead", \
                     "1BDISNA-Disabled Joint Owner Homestead Non AG", "1BDISAG-Disabled Joint Owner Homestead Ag", "1BAG-Blind/Disabled Homestead Ag", \
                     "VET FULL HSTD", "Owner Homestead (may be partial)", "1" )
    #Sets values to look for in the original field to set the values in the new field to M for maybe
    Homestead_Maybe = ("FRACTIONAL", "BD  HOMESTEAD", "BD MID YEAR", "MID YEAR", "FRACT HOMESTEAD", "BPVD HOMESTEAD", \
                       "BPVD FRACT HSTD", "MID-YR HSTD")
    #Looks for values in the original field to set values in the new field to No
    Homestead_No = ("Non Homestead", "", " ", "N", "0", "NON-HOMESTEAD", "4C12-Seasonal recreational residential - Non Commercial", \
                    "4C1COMM-Seasonal recreational residential - Comm", "4C2-Qualifying golf courses", "4C3-Nonprofit community service oriented org - Non Revenue", \
                    "4C3DONAT - Nonprofit community service oriented org - Donations", "4C5-Manufactured home parks", \
                    "4C5COOP1-Manufactured home parks coop > 50% Shareholder Occupanc", "4D-Qual. Low Income-Land/Bldg", \
                    "52OPNIOC-All other property not included in any other", "5E-Exempt Properties", "PILT-Payment In-Lieu of Taxes", \
                    "4BB-Residential Non-Homestead SFD", "4B4-Residential nonhomestead - Land only", "3A-Commercial/Industrial/Public Utility", \
                    "2CMFL-Managed Forest Land", "2B-Rural Vacant Land/Non-Productive - Non Homestead", "2B-Rural Vacant Land/Non-Productive - Homestead", \
                    "2AREM-Agricultural Homestead - Remainder", "2ANHGA-Agricultural Non-homestead - Non HGA", "1C-Commercial seasonal - residential recreational", \
                    "4D-Qual. Low Income-Land/Bldg", "4C5-Manufactured home parks", "4C3DONAT - Nonprofit community service oriented org - Donations", \
                    "4BB2-Ag HGA Non Homestead", "NON HOMESTEAD")
    #Sets values in the Use Description fields to look for to set the Rental field to yes
    Use_Rental_Yes = ("Residential Non-hstd 1-3 Units not 4bb", "Residential Non-Homestead (Single Unit)", "Qual Low Income Rental Housing - 4+ units", "Elderly Living Facility", \
                      "Apartment (4 or more units)", "Assisted Living Apartments", "Apartment", "Indian Reservation - Residential", "205", "COMM LAND &amp; BLDGS,RES 1-3 UNITS", \
                      "COMM LAND &amp; BLDGS,RES 4 OR MORE UNITS", "COMM LAND &amp; BLDGS,RES 4 OR MORE UNITS,RES 4+ OWNERS VALUE", "COMM LAND &amp; BLDGS,RES DUPLEX/TRIPLEX", \
                      "COMM LAND &amp; BLDGS,RESIDENTIAL", "TRANSITIONAL HOUSING", "4 OR MORE UNITS", "1 TO 3 UNIT DWELLING", "MIGRANT HOUSING", "QUALIFING 4D LOW INCOME", \
                      "RESIDENTIAL TRIPLEX", "4C4-Post secondary student housing", "4BB-Residential Non-Homestead SFD", "4B1-Residential Non-Homestead 3 Units or less" , \
                      "4A-Rental/Residential Non-Homestead 4 or More Unit", "Residential 2-3 units or Vacant Land", "Qual Low Income Rental Housing - 4+ units", "204", "Residential Non-Homestead (Single Unit)", \
                      "APARTMENTS / COOP, COMMERCIAL / GOLF COURSE,", "APARTMENTS / COOP, APARTMENTS / COOP, COMMERCIAL / GOLF COURSE,", "APARTMENTS / COOP, APARTMENTS / COOP, APARTMENTS / COOP,", \
                      "APARTMENTS / COOP, APARTMENTS / COOP,", "APARTMENTS / COOP", "Apt 4+ units", "APARTMENT", "Apartment", "Apartment Condominium", "110 Apt 4+ units", \
                      "110 Apt 4+ units/300 Commercial", "110")
    #Sets values to look in the Use Description fields to look for to set the Rental field to Maybe
    Use_Rental_Maybe = ("RES 1-3 UNITS", "RES 4 OR MORE UNITS", "RES 4+ OWNERS VALUE", "RES DUPLEX/TRIPLEX", "RES/AG", "RESIDENTIAL", "4D 4 OR MORE UNITS", "CHURCH,RES", \
                        "AG DUPLEX/TRIPLEX", "Two-Family Flat", "Two-Family Duplex", "Two-Family Conversion", "Townhouse", "Three-Family Conversion", "Six-Family Conversion", \
                        "Single-Family / Unit", "Single-Family", "Four-Family Conversion", "RESIDENTIAL SINGLE FAMILY, RESIDENTIAL SINGLE FAMILY,", "RESIDENTIAL SINGLE FAMILY", \
                        "RESIDENTIAL DUPLEXES, DOUBLE BUNGALOWS,", "MANUFACTURED HOME PARK, RESIDENTIAL SINGLE FAMILY,", "INDUSTRIAL, RESIDENTIAL SINGLE FAMILY,", "CONDOMINIUMS", \
                        "COMMERCIAL / GOLF COURSE, RESIDENTIAL SINGLE FAMILY, RESIDENTIAL SINGLE FAMILY,", "COMMERCIAL / GOLF COURSE, RESIDENTIAL SINGLE FAMILY,", \
                        "COMMERCIAL / GOLF COURSE, RESIDENTIAL DUPLEXES, DOUBLE BUNGALOWS,", "COMMERCIAL / GOLF COURSE, MANUFACTURED HOME PARK, RESIDENTIAL SINGLE FAMILY,", \
                        "Res 2-3 units", "Res 1 unit", "Trans Housing", "RESIDENTIAL-TOWNHOUSE", "APARTMENT-NURSING HOME", "APARTMENT-MOBILE HOME PARK", "Triplex", "Townhouse", \
                        "Condo Garage/Miscellaneous", "Condominium", "Double Bungalow", "Farm-Hmstd (House & 1 Acre)", "Housing - Low Income < 4 Units", "Housing - Low Income > 3 Units", \
                        "Mobile Home Park", "Nursing Home", "Residential", "Residential", "Sorority/Fraternity Housing", "College-Priv Res", "Schools-Priv Res", "Schools-Pub Res", \
                        "925 Trans Housing", "922 Hosp-Pub Res", "917 Church-Other Res", "916 Church-Residence/915 Church/902 Schools-Private", "916 Church-Residence", "915 Church/916 Church-Residence", \
                        "906 Schools-Pub Res", "350 MH Park/100 Res 1 unit", "305 Industrial/100 Res 1 unit", "300 Commercial/200 Agricultural/100 Res 1 unit", "300 Commercial/110 Apt 4+ units", \
                        "300 Commercial/105 Res 2-3 units", "300 Commercial/100 Res 1 unit/200 Agricultural", "300 Commercial/100 Res 1 unit", "200 Agricultural/300 Commercial/100 Res 1 unit", \
                        "200 Agricultural/105 Res 2-3 units", "200 Agricultural/100 Res 1 unit/105 Res 2-3 units", "200 Agricultural/100 Res 1 unit", "110 Apt 4+ units/931 Charit Inst", \
                         "105 Res 2-3 units/300 Commercial/200 Agricultural", "105 Res 2-3 units/300 Commercial", "105 Res 2-3 units/200 Agricultural", "105 Res 2-3 units", \
                        "100 Res 1 unit/300 Commercial", "100 Res 1 unit/200 Agricultural", "100 Res 1 unit/115 B & B", "100 Res 1 unit/105 Res 2-3 units", "100 Res 1 unit", \
                        "RES X-TRA FUL", "RESIDENTIAL\S", "RESIDENTIAL T", "100", "105", "200", "210")
    #Sets values to look for in the Use Description fields to set the homestead field to Y, if there is not homestead field
    Use_Home = ("Residential 2-3 units or Vacant Land", "Residential 1 unit Previously SRR", "Residential 1 unit", "102", "106", "201", "202", "203", "206", "AGRICULTURAL,RESIDENTIAL", \
                "AGRICULTURAL,COMM LAND &amp; BLDGS,RESIDENTIAL", "AGRICULTURAL,MANURE PITS,RES/AG", "AGRICULTURAL,MANURE PITS,RESIDENTIAL", "CHURCH-OTHER,RES", "CHURCH,CHURCH,RES", \
                "CHURCH,RES", "RESIDENTIAL\SINGLE UNIT", "2AREM-Agricultural Homestead - Remainder", "2AHGA-Agricultural Homestead - HGA", "1BREM-Blind/Disabled Homestead Ag Remainder", \
                "1A-Residential Homestead", "Residential Hstd 1 Unit in Apartment", "100 Res 1 unit")
    #Sets values in the Homestead field to look for in the homestead field that will set the rental field to Y
    Homestead_Rental = ("4B1-Residential Non-Homestead 3 Units or less", "4A-Rental/Residential Non-Homestead 4 or More Unit", "4BB1-Residential Non-Homestead single unit", \
                        "RESIDENTIAL", "Church-Residence", "Church-Other Res", "Charit Inst-Res")
    #Creates a list of feature classes
    fclist = arcpy.ListFeatureClasses("*", '')
    for fc in fclist:
        # Adds a Rental field to hold the Y and N values based on the values of the original fields
        arcpy.AddField_management(fc, "RENTAL", "TEXT", "", "", 100, "RENTAL")
        #Adds a Homestead field to hold the Homestead Yes and No values
        arcpy.AddField_management(fc, "HOMESTEAD_YN", "TEXT", "", "", 100, "HOMESTEAD_YN")
        print fc
        #Creates a variable for the full path of the feature class
        Feature = workspace + "\\" + fc
        #Creates a list of all of the fields in the feature classes
        fieldlist = arcpy.ListFields(Feature)
        #Creates a generator expression for all of the fields names in the feature class
        fields = [f.name for f in fieldlist]
        #If the feature class has a homestead field, but not Use Description fields
        if "HOMESTEAD" in fields and "USE1_DESC" not in fields:
            #These fields will be used in the cursor
            Fields = ("HOMESTEAD", "HOMESTEAD_YN", "RENTAL")
            #Creates the cursor that loops through the homestead field
            Home_Cursor = arcpy.da.UpdateCursor(fc, Fields)
            for row in Home_Cursor:
                    #Sets a variable to the homestead fiedl
                    Homestead = row[0]
                    #If Homestead is Null, it updates it to blank
                    if Homestead is None:
                        row[0] = ""
                        Home_Cursor.updateRow(row)
                    #If value is in Homestead Yes, Homestead YN is updated to yes
                    elif Homestead in Homestead_Yes:
                        row[1] = "Y"
                        Home_Cursor.updateRow(row)
                    #If value is a number and above 0, then Homestead YN is updated to Yes
                    elif Homestead.isdigit() and int(Homestead) > 0:
                        row[1] = "Y"
                        Home_Cursor.updateRow(row)
                    #If Homestead is in Homestead Maybe, Homestead YN is updated to maybe
                    elif Homestead in Homestead_Maybe:
                        row[1] = "M"
                        Home_Cursor.updateRow(row)
                    #If value is in Homestead Rental, Rental is upated to Y
                    elif Homestead in Homestead_Rental:
                        row[2] = "Y"
                        row[1] = "N"
                        Home_Cursor.updateRow(row)
                    else:
                        #If value is in Homestead No, Homestead YN is updated to N
                        if Homestead in Homestead_No:
                            row[1] = "N"
                            Home_Cursor.updateRow(row)
        #If there is a Use Description field in the list of fields
        elif "USE1_DESC" in fields:
            #If there is a Use Description One and an Use Desription Two Field
            if "USE1_DESC" in fields and "USE2_DESC" in fields:
                #If there is a Use Description One, a Use Description Two, and a Use Description Three field
                if "USE1_DESC" in fields and "USE2_DESC" in fields and "USE3_DESC" in fields:
                    #If there is a Use Description One, a Use Description Two, A use Description three, and a Use Description Four field
                    if "USE1_DESC" in fields and "USE2_DESC" in fields and "USE3_DESC" and "USE4_DESC" in fields:
                        #This sequence is the same from before
                        if "HOMESTEAD" in fields:
                            Fields = ("HOMESTEAD", "HOMESTEAD_YN", "RENTAL")
                            Home_Cursor = arcpy.da.UpdateCursor(fc, Fields)
                            for row in Home_Cursor:
                                Homestead = row[0]
                                if Homestead is None:
                                    row[0] = ""
                                    Home_Cursor.updateRow(row)
                                elif Homestead in Homestead_Yes:
                                    row[1] = "Y"
                                    Home_Cursor.updateRow(row)
                                elif Homestead.isdigit() and int(Homestead) > 0:
                                    row[1] = "Y"
                                    Home_Cursor.updateRow(row)
                                elif Homestead in Homestead_Maybe:
                                    row[1] = "M"
                                    Home_Cursor.updateRow(row)
                                elif Homestead in Homestead_Rental:
                                    row[2] = "Y"
                                    row[1] = "N"
                                    Home_Cursor.updateRow(row)
                                else:
                                    if Homestead in Homestead_No:
                                        row[1] = "N"
                                        Home_Cursor.updateRow(row)
                        cursorfields = ("HOMESTEAD", "USE1_DESC", "USE2_DESC", "USE3_DESC", "USE4_DESC", "HOMESTEAD_YN", "RENTAL")
                        RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                        for row in RentCursor:
                            Home = row[0]
                            Use1 = row[1]
                            Use2 = row[2]
                            Use3 = row[3]
                            Use4 = row[4]
                            HomeYN = row[5]
                            Rent = row[6]
                            if HomeYN == "Y":
                                row[6] = "N"
                                RentCursor.updateRow(row)
                            elif HomeYN == "N":
                                if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes or Use3 in Use_Rental_Yes or Use4 in Use_Rental_Yes:
                                    row[6] = "Y"
                                    RentCursor.updateRow(row)
                                elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe or Use3 in Use_Rental_Maybe or Use4 in Use_Rental_Maybe:
                                    row[6] = "Y"
                                    RentCursor.updateRow(row)
                                else:
                                    row[6] = "N"
                                    RentCursor.updateRow(row)
                            elif HomeYN is None:
                                if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes or Use3 in Use_Rental_Yes or Use4 in Use_Rental_Yes:
                                    row[5] = "N"
                                    row[6] = "Y"
                                    RentCursor.updateRow(row)
                                elif Use1 in Use_Home or Use2 in Use_Home or Use3 in Use_Home or Use4 in Use_Home:
                                    row[5] = "Y"
                                    row[6] = "N"
                                    RentCursor.updateRow(row)
                                elif Use1 in Use_Rental_Maybe:
                                    row[5] = "M"
                                    row[6] = "M"
                                    RentCursor.updateRow(row)
                                else:
                                    row[5] = "N"
                                    row[6] = "N"
                                    RentCursor.updateRow(row)
                    else:
                        cursorfields = ("USE1_DESC", "USE2_DESC", "USE3_DESC", "USE4_DESC", "HOMESTEAD_YN", "RENTAL")
                        RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                        for row in RentCursor:
                            Use1 = row[0]
                            Use2 = row[1]
                            Use3 = row[2]
                            Use4 = row[3]
                            HomeYN = row[4]
                            Rent = row[5]
                            if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes or Use3 in Use_Rental_Yes or Use4 in Use_Rental_Yes:
                                row[4] = "N"
                                row[5] = "Y"
                                RentCursor.updateRow(row)
                            elif Use1 in Use_Home or Use2 in Use_Home or Use3 in Use_Home or Use4 in Use_Home:
                                row[4] = "Y"
                                row[5] = "N"
                                RentCursor.updateRow(row)
                            elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe or Use3 in Use_Rental_Maybe or Use4 in Use_Rental_Maybe:
                                row[4] = "M"
                                row[5] = "M"
                                RentCursor.updateRow(row)
                            else:
                                row[4] = "N"
                                row[5] = "N"
                                RentCursor.updateRow(row)
                else:
                    if "HOMESTEAD" in fields:
                        if field.name == "HOMESTEAD":
                            Fields = ("HOMESTEAD", "HOMESTEAD_YN", "RENTAL")
                            Home_Cursor = arcpy.da.UpdateCursor(fc, Fields)
                            for row in Home_Cursor:
                                Homestead = row[0]
                                if Homestead is None:
                                    row[0] = ""
                                    Home_Cursor.updateRow(row)
                                elif Homestead in Homestead_Yes:
                                    row[1] = "Y"
                                    Home_Cursor.updateRow(row)
                                elif Homestead.isdigit() and int(Homestead) > 0:
                                    row[1] = "Y"
                                    Home_Cursor.updateRow(row)
                                elif Homestead in Homestead_Maybe:
                                    row[1] = "M"
                                    Home_Cursor.updateRow(row)
                                elif Homestead in Homestead_Rental:
                                    row[2] = "Y"
                                    row[1] = "N"
                                    Home_Cursor.updateRow(row)
                                else:
                                    if Homestead in Homestead_No:
                                        row[1] = "N"
                                        Home_Cursor.updateRow(row)
                        cursorfields = ("HOMESTEAD", "USE1_DESC", "USE2_DESC", "USE3_DESC", "HOMESTEAD_YN", "RENTAL")
                        RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                        for row in RentCursor:
                            Home = row[0]
                            Use1 = row[1]
                            Use2 = row[2]
                            Use3 = row[3]
                            HomeYN = row[4]
                            Rent = row[5]
                            if HomeYN == "Y":
                                row[5] = "N"
                                RentCursor.updateRow(row)
                            elif HomeYN == "N":
                                if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes or Use3 in Use_Rental_Yes:
                                    row[5] = "Y"
                                    RentCursor.updateRow(row)
                                elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe or Use3 in Use_Rental_Maybe:
                                    row[5] = "Y"
                                    RentCursor.updateRow(row)
                                else:
                                    row[5] = "N"
                                    RentCursor.updateRow(row)
                            elif HomeYN is None:
                                if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes or Use3 in Use_Rental_Yes:
                                    row[4] = "N"
                                    row[5] = "Y"
                                    RentCursor.updateRow(row)
                                elif Use1 in Use_Home or Use2 in Use_Home or Use3 in Use_Home:
                                    row[4] = "Y"
                                    row[5] = "N"
                                    RentCursor.updateRow(row)
                                elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe or Use3 in Use_Rental_Maybe:
                                    row[4] = "M"
                                    row[5] = "M"
                                    RentCursor.updateRow(row)
                                else:
                                    row[4] = "N"
                                    row[5] = "N"
                                    RentCursor.updateRow(row)
                    else:
                        cursorfields = ("USE1_DESC", "USE2_DESC", "USE3_DESC", "HOMESTEAD_YN", "RENTAL")
                        RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                        for row in RentCursor:
                            Use1 = row[0]
                            Use2 = row[1]
                            Use3 = row[2]
                            HomeYN = row[3]
                            Rent = row[4]
                            if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes or Use3 in Use_Rental_Yes:
                                row[3] = "N"
                                row[4] = "Y"
                                RentCursor.updateRow(row)
                            elif Use1 in Use_Home or Use2 in Use_Home or Use3 in Use_Home:
                                row[3] = "Y"
                                row[4] = "N"
                                RentCursor.updateRow(row)
                            elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe or Use3 in Use_Rental_Maybe:
                                row[3] = "M"
                                row[4] = "M"
                                RentCursor.updateRow(row)
                            else:
                                row[3] = "N"
                                row[4] = "N"
                                RentCursor.updateRow(row)
            else:
                if "HOMESTEAD" in fields:
                    Fields = ("HOMESTEAD", "HOMESTEAD_YN", "RENTAL")
                    Home_Cursor = arcpy.da.UpdateCursor(fc, Fields)
                    for row in Home_Cursor:
                        Homestead = row[0]
                        if Homestead is None:
                            row[0] = ""
                            Home_Cursor.updateRow(row)
                        elif Homestead in Homestead_Yes:
                            row[1] = "Y"
                            Home_Cursor.updateRow(row)
                        elif Homestead.isdigit() and int(Homestead) > 0:
                            row[1] = "Y"
                            Home_Cursor.updateRow(row)
                        elif Homestead in Homestead_Maybe:
                            row[1] = "M"
                            Home_Cursor.updateRow(row)
                        elif Homestead in Homestead_Rental:
                            row[2] = "Y"
                            row[1] = "N"
                            Home_Cursor.updateRow(row)
                        else:
                            if Homestead in Homestead_No:
                                row[1] = "N"
                                Home_Cursor.updateRow(row)
                cursorfields = ("HOMESTEASD", "USE1_DESC", "USE2_DESC", "HOMESTEAD_YN", "RENTAL")
                RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                for row in RentCursor:
                    Home = row[0]
                    Use1 = row[1]
                    Use2 = row[2]
                    HomeYN = row[3]
                    Rent = row[4]
                    if HomeYN == "Y":
                        row[5] = "N"
                        RentCursor.updateRow(row)
                    elif Home == "N":
                        if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes:
                            row[4] = "Y"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe:
                            row[4] = "Y"
                            RentCursor.updateRow(row)
                        else:
                            row[4] = "N"
                            RentCursor.updateRow(row)
                    elif HomeYN is None:
                        if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes:
                            row[3] = "N"
                            row[4] = "Y"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Home or Use2 in Use_Home:
                            row[3] = "Y"
                            row[4] = "N"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe:
                            row[3] = "M"
                            row[4] = "M"
                            RentCursor.updateRow(row)
                        else:
                            row[3] = "N"
                            row[4] = "N"
                            RentCursor.updateRow(row)
                else:
                    cursorfields = ("USE1_DESC", "USE2_DESC", "HOMESTEAD_YN", "RENTAL")
                    RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                    for row in RentCursor:
                        Use1 = row[0]
                        Use2 = row[1]
                        HomeYN = row[2]
                        Rent = row[3]
                        if Use1 in Use_Rental_Yes or Use2 in Use_Rental_Yes:
                            row[1] = "N"
                            row[2] = "Y"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Home or Use2 in Use_Home:
                            row[1] = "Y"
                            row[2] = "N"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Rental_Maybe or Use2 in Use_Rental_Maybe:
                            row[1] = "M"
                            row[2] = "M"
                            RentCursor.updateRow(row)
                        else:
                            row[1] = "N"
                            row[2] = "N"
                            RentCursor.updateRow(row)
        else:
            if "HOMESTEAD" in fields:
                Fields = ("HOMESTEAD", "HOMESTEAD_YN", "RENTAL")
                Home_Cursor = arcpy.da.UpdateCursor(fc, Fields)
                for row in Home_Cursor:
                    Homestead = row[0]
                    if Homestead is None:
                        row[0] = ""
                        Home_Cursor.updateRow(row)
                    elif Homestead in Homestead_Yes:
                        row[1] = "Y"
                        Home_Cursor.updateRow(row)
                    elif Homestead.isdigit() and int(Homestead) > 0:
                        row[1] = "Y"
                        Home_Cursor.updateRow(row)
                    elif Homestead in Homestead_Maybe:
                        row[1] = "M"
                        Home_Cursor.updateRow(row)
                    elif Homestead in Homestead_Rental:
                        row[2] = "Y"
                        row[1] = "N"
                        Home_Cursor.updateRow(row)
                    else:
                        if Homestead in Homestead_No:
                            row[1] = "N"
                            Home_Cursor.updateRow(row)
            cursorfields = ("HOMESTEAD", "USE1_DESC", "HOMESTEAD_YN", "RENTAL")
            RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
            for row in RentCursor:
                Home = row[0]
                Use1 = row[1]
                HomeYN = row[2]
                Rent = row[3]
                if HomeYN == "Y":
                    row[3] = "N"
                    RentCursor.updateRow(row)
                elif HomeYN == "N":
                    if Use1 in Use_Rental_Yes:
                        row[3] = "Y"
                        RentCursor.updateRow(row)
                    elif Use1 in Use_Rental_Maybe:
                        row[3] = "Y"
                        RentCursor.updateRow(row)
                    else:
                        row[3] = "N"
                        RentCursor.updateRow(row)
                elif HomeYN is None:
                    if Use1 in Use_Rental_Yes:
                        row[2] = "N"
                        row[3] = "Y"
                        RentCursor.updateRow(row)
                    elif Use1 in Use_Home:
                        row[2] = "Y"
                        row[3]= "N"
                        RentCursor.updateRow(row)
                    elif Use1 in Use_Rental_Maybe:
                        row[2] = "M"
                        row[3] = "M"
                        RentCursor.updateRow(row)
                    else:
                        row[3] = "N"
                        row[2] = "N"
                        RentCursor.updateRow(row)
                else:
                    cursorfields = ("USE1_DESC", "HOMESTEAD_YN", "RENTAL")
                    RentCursor = arcpy.da.UpdateCursor(fc, cursorfields)
                    for row in RentCursor:
                        Use1 = row[0]
                        HomeYN = row[1]
                        Rent = row[2]
                        if Use1 in Use_Rental_Yes:
                            row[1] = "N"
                            row[2] = "Y"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Home:
                            row[1] = "Y"
                            row[2] = "N"
                            RentCursor.updateRow(row)
                        elif Use1 in Use_Rental_Maybe:
                            row[1] = "M"
                            row[2] = "M"
                            RentCursor.updateRow(row)
                        else:
                            row[1] = "N"
                            row[2] = "N"
                            RentCursor.updateRow(row)




