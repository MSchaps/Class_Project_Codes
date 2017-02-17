#This script contains a module that renames all of the fields that are going to be needed in the analysis to a standard name that can be queryed later
def Field_Renamer(workspace, CountyCodeDict):
    import arcpy
    from arcpy import env
    #Sets the workspace to the geodatabase that contains the original parcels
    env.workspace = workspace
    env.overwriteOutput = True
    import unicodedata
    #Creates a dictionary that holds what the homestead field for each feature class is. The County Fips code for each county is linked to
    #the homestead field, which is used to reduce the overall length of the dictionary. What may seem strange at first is the inclusion of the
    #first entry in the dictionary: A key called "Name". This is used later on.
    HomesteadDict = {"Name":"HomesteadDict", "001":"TPHSTC", "007":"HOMESTEAD", "009":"C0EXCLHSTD", "011":"Homestead", "015":"HOMESTEAD", "017":"TPHSTC", "025":"HomeCd1", \
                     "029":"HomesteadC", "039":"C0HSTDDS", "041":"PVHSTD", "043":"HOMESTEAD", "061":"HSTD_CODE", "071":"HSTDCODE", "079":"HST_Code", "083":"Hstddesc",  \
                     "111":"H_Cd","115":"HOMESTEAD", "117":"HOMESTEAD", "119":"Homestead", "137":"HSTD_Desc1", "147":"AVHSTCDESC", "153" :"TPHST1", "157":"HOMESTEAD", "169":"Tax_Cama_3"}
    # Creates a dictionary that holds what the Use Class 1 field for each feature class is. The County Fips code for each county is linked to
    # the homestead field, which is used to reduce the overall length of the dictionary. What may seem strange at first is the inclusion of the
    # first entry in the dictionary: A key called "Name". This is used later on.
    LandUse1Dict = {"Name":"LandUse1Dict", "001":"TPCLS1", "007":"USE1_DESC", "009":"C0CLSFDS", "013":"Occupancy", "015":"CLASS", "017":"TPCLS1", \
                    "023":"CLASSFICAT", "025":"ClassCd1", "029":"Classifica", "033":"propclass", "041":"PVCLSD", "043":"USE1_DESC", "061":"CLASS_CODE", "071":"ClassCd1", \
                    "075":"Class", "079":"CLS_Code", "083":"Asmtdesc", \
                    "097":"PriClass", "111":"ClassDesc", "115":"CLASS_1", "117":"Class", "119":"Class", "131":"CLASS", "137":"TPCLS1", "141":"CLS_DESC", "143":"CLASSIFICA", "145":"PROPCLASSL", "147":"AVCLASDESC", "153":"TPASM1", \
                    "157":"CLASSIFICA", "161":"TAXCLASS", "169":"PRClass", "169":"Tax_Cama_2", "171":"PRClass"}
    # Creates a dictionary that holds what the Use Class 1 field for each feature class is. The County Fips code for each county is linked to
    # the homestead field, which is used to reduce the overall length of the dictionary. What may seem strange at first is the inclusion of the
    # first entry in the dictionary: A key called "Name". This is used later on.
    LandUse2Dict = {"Name":"LandUse2Dict", "001": "TPCLS2", "007":"USE2_DESC", "023":"CLASSIFICA", "025":"ClassCd2", "029":"Classifi_1", \
                    "071":"ClassCd2", "075":"Class2", "097":"SecClass", "131":"Class2", "137":"TPCLS2", "147":"AVCLASDE_1"}
    # Creates a dictionary that holds what the Use Class 3 field for each feature class is. The County Fips code for each county is linked to
    # the homestead field, which is used to reduce the overall length of the dictionary. What may seem strange at first is the inclusion of the
    # first entry in the dictionary: A key called "Name". This is used later on.
    LandUse3Dict = {"Name":"LandUse3Dict", "001": "TPCLS3", "007":"USE3_DESC", "023":"CLASSIFI_1", "025":"ClassCd3", "029":"Classifi_2", \
                    "071":"CLASSCODE3", "075":"Class3", "097":"ThirdClass", "131":"Class3", "137":"TPCLS3", "147":"AVCLASDE_2"}
    # Creates a dictionary that holds what the Use Class 4 field for each feature class is. The County Fips code for each county is linked to
    # the homestead field, which is used to reduce the overall length of the dictionary. What may seem strange at first is the inclusion of the
    # first entry in the dictionary: A key called "Name". This is used later on.
    LandUse4Dict = {"Name":"LandUse4Dict", "007":"USE4_DESC", "025":"ClassCd4","029":"Classifi_3", "075":"Class4", "131":"Class4"}
    #This creates a dictionary that contains what the fields contained in each dictionary should be standardized to based on the "Name" of the
    #dictionary. Now, any one that knows anything about python may know that dictionaries, by default, do not have any comprehension of their intial
    #name. This becomes a problem in a future portion of the script. To overcome this, I set a key in each dictionary that contains a callable
    #"Name".
    Field_Name_Dict = {"HomesteadDict":"HOMESTEAD", "LandUse1Dict":"USE1_DESC", "LandUse2Dict":"USE2_DESC", "LandUse3Dict":"USE3_DESC", \
                       "LandUse4Dict":"USE4_DESC"}
    #Creates a list of the dictionaries to be used later
    dictlist = [HomesteadDict, LandUse1Dict, LandUse2Dict,  LandUse3Dict, LandUse4Dict]
    fclist = arcpy.ListFeatureClasses("*", "")
    #Creates a list of all of the feature classes in the input geodatabase
    for fc in fclist:
        #Creates a variable for the path to each feature class
        Feature = workspace + "\\" + fc
        #Creates a variable for the name of the feature class
        Feature_Full_Name = unicodedata.normalize('NFKD', fc).encode('ascii', 'ignore')
        #Creates a variable for the county name, split from _Parcels
        Feature_Name = Feature_Full_Name.split('_Parcels', 1)[0]
        #Retrieves the County Code from the County Code Dictionary
        Code = CountyCodeDict[Feature_Name]
        #Creates a list of the fields in each of the feature classes
        fieldlist = arcpy.ListFields(Feature)
        #This is a generator expression that creates a list of all of the field names in each feature class
        fields = [field.name for field in fieldlist]
        for dict in dictlist:
            #Calls the dictionary with the final standardized field names. This is technically a nested dictionary call, because
            #the one dictionary is being called by calling the name key of the rest of the dictionaries
            Field_Name = Field_Name_Dict[dict["Name"]]
            #If the county does not have a listed field name for of each of the dictionaries, it is skipped
            if Code not in dict:
                print fc + " Does Not Have Known " + Field_Name + "Field on Record"
                pass
            else:
                #if the field is already in the feature class with the correct names, it is skipped
                if Field_Name in fields:
                    pass
                else:
                    print fc
                    #Calls each dictionary individually with the County Codes. This allows for one dictionary calling module instead of five
                    dictfield = dict[Code]
                    # print ZIP
                    for field in fieldlist:
                        print fc + " has" + Field_Name + " field but it is incorrectly named"
                        print "Changing city field for " + fc
                        #Changes the field name of each field in the feature classes to the standardized namwe
                        arcpy.AlterField_management(Feature, dictfield, Field_Name, Field_Name)
                        print Field_Name + " changed from " + dictfield + " to " + Field_Name + " for " + fc
                        break
