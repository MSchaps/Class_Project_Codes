## This script is the master trigger for all of the other modules that make up this script. This way, instead of having a very long singular script of
## either separate modules or a class, you instead have only one small script that you need to initialize/set up the inputs to. All of the modules held
##inside of the other scripts are brought into this modules, and ran in the order that they need to be for the desired output to happen. What is important
## to note is that for this script to work, all of the imported scripts must be included within the same folder as the master module.
def Master(workspace, Final_Path, GDB_Name):
    #These import statements bring in all of the other modules
    import Reprojector
    import Homestead_Formatter
    import Type_Changer
    import Value_Changer
    import Parcel_Selector
    import Field_Deleter
    import Euclidean_Generator
    import Value_Joiner
    import Reclassify_Values
    #This dictionary is used in the field renaming module. It links the name of each parcel feature class. As long
    #as a feature class is named with the convention "County Name" + "_" + "Parcels, it will work with this dictionary,
    #and this process is explained later.
    CountyCodeDict = {"Aitkin": "001", "Anoka": "003", "Becker": "005", "Beltrami": "007", "Bemidji": "007",
                      "Benton": "009", "Big_Stone": "011", "Blue_Earth": "013", "Brown": "015", "Carlton": "017", \
                      "Carver": "019", "Cass": "021", "Chippewa": "023", "Chisago": "025", "Clay": "027", \
                      "Clearwater": "029", "Cook": "031", "Cottonwood": "033", "Crow_Wing": "035", "Dakota": "037",
                      "Dodge": "039", "Douglas": "041", "Faribault": "043", "Fillmore": "045", "Freeborn": "047", \
                      "Goodhue": "049", "Grant": "051", "Hennepin": "053","Houston": "055", "Hubbard": "057", \
                      "Isanti": "059", "Itasca": "061", "Jackson": "063", "Kanabec": "065", "Kandiyohi": "067", \
                      "Kittson": "069","Koochiching": "071", "Lac_Qui_Parle": "073", "Lake": "075", \
                      "Lake_of_the_Woods": "077", "Le_Sueur": "079", "Lincoln": "081", "Lyon": "083","McLeod": "085", \
                      "Mahnomen": "087", "Marshall": "089", "Martin": "091", "Meeker": "093", "Mille_Lacs": "095", \
                      "Morrison": "097", "Mower": "099", "Murray": "101", "Nicollet": "103", "Nobles": "105", "Norman": "107", \
                      "Olmsted": "109", "Otter_Tail": "111", "Pennington": "113", "Pine": "115", "Pipestone": "117", "Polk": "119", \
                      "Pope": "121", "Ramsey": "123", "Red_Lake": "125", "Redwood": "127", "Renville": "129",
                      "Rice": "131", "Rock": "133", "Roseau": "135", "Saint_Louis": "137", "Scott": "139", "Sherburne": "141", \
                      "Sibley": "143", "Stearns": "145", "Steele": "147", "Stevens": "149", "Swift": "151", "Todd": "153", \
                      "Traverse": "155", "Wabasha": "157", "Wadena": "159", "Waseca": "161", "Washington": "163", "Watonwan": "165", \
                      "Wilkin": "167", "Winona": "169", "Wright": "171", "Yellow_Medicine": "173"}
    #This is an input for the geodatabse that will hold the final outputted feature classes. It is created by combining the folder that you
    #want the geodatabase holds the final outputs, and the name of the final geodatabase.
    final_workspace = Final_Path + "\\" + GDB_Name
    #This calls the module that reprojects all of the input parcels, and the business points to NAD 1983 UTM Zone 15 N. This is important due to
    #future joins in the scripts being based on spatial location.
    Reprojector.ReprojectData(workspace)
    #This calls the module that takes all of the relevant fields that will be needed in the analysis, and changes all of them into a standard name
    Homestead_Formatter.Field_Renamer(workspace,CountyCodeDict)
    #This calls a module that takes all of the now standardized named fields that are relevant for the analysis, and changes all of them to a conssitent
    #type. This is important for the future querying of the data.
    Type_Changer.FieldTypeChanger(workspace)
    #This calls the module that adds two new fields that hold the rental and homestead status of the parcels. It also parses through the existing values
    #and populates the field based on certain values in the fields.
    Value_Changer.FieldTypeChanger(workspace)
    #This calls a module that parses through the newly added fields, and selects out the relevant parcels based on the values of these fields
    Parcel_Selector.Parcel_Selector(workspace, Final_Path, GDB_Name)
    #This calls a module that goes through the newly created feature classes, and deletes fields in the that I have been instructed by various counties not to
    #make public
    Field_Deleter.Field_Deleter(final_workspace)
    #This calls a module that generates euclidean distances analyses from the businesses in the geodatabase, and creates the outputs in the workspace.
    Euclidean_Generator.Eudlidean_Generator(business_workspace, final_workspace)
    #This calls a module that joins the values of the rasters to the parcel feature classes
    Value_Joiner.Value_Joiner(final_workspace)
    #This calls a module that creates a field that holds the finals "score" values of the parcels based on the distances from each of the businesses
    Reclassify_Values.Value_Reclassify(final_workspace)

#These are the needed inputs for all of the modules. The first is the original geodatabase that holds the original parcels
workspace = r'C:\GIS\Advanced_Geocomputing\Final_Project\Last_Test.gdb'
#This is the location where the final geodatabase will be placed
Final_Path = r'C:\\GIS\\Advanced_Geocomputing\\Final_Project'
#This is the name of the final geodatabase
GDB_Name = r'Final.gdb'
#This is the geodatabase that holds the business dara
business_workspace = r'C:\GIS\Advanced_Geocomputing\Final_Project\Businesses_7_County.gdb'
Master(workspace, Final_Path, GDB_Name)
