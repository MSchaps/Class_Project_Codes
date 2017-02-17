#This script changes the type of each of the fields with the standard name to one consistent type. This will make future querying of the
#values easier
def FieldTypeChanger(workspace):
    import arcpy
    #This dictionary contains what the type of each of the standard fields should be. This is called later on
    field_type_dict = {"USE1_DESC":"TEXT", "USE2_DESC":"TEXT", "USE3_DESC":"TEXT", "USE4_DESC":"TEXT", "HOMESTEAD":"TEXT"}
    #This dictionary contains the length of the new fields that will be created in the type changing process
    field_length_dict = {"USE1_DESC":100, "USE2_DESC":100, "USE3_DESC":100, "USE4_DESC":100, "HOMESTEAD":100}
    from arcpy import env
    #Sets the workspace to the input geodatabase containing the parcels
    env.workspace = workspace
    #Sets Overwrite Outputs to true
    env.overwriteOutput = True
    #Creates a litst of all of the feature classes in the geodatabase
    fclist = arcpy.ListFeatureClasses("*", '')
    for fc in fclist:
        print fc
        # Creates a variable for the full path to the feature class.
        Feature = workspace + "\\" + fc
        #Creates a litst of all of the fields in the feature classes
        fieldlist = arcpy.ListFields(Feature)
        #Creates a generator expression that contains the names of all of the fields in the feature classes
        fields = [f.name for f in fieldlist]
        #Loops through all of the fields
        for field in fieldlist:
            #If the field name is in the field type dictionary
            if field.name in field_type_dict:
                #calls the field type dictionary to know what type the standard field should be
                Field_type = field_type_dict[str(field.name)]
                print field.name
                print field.type
                print Field_type
                #This deletes a field called temp if it already exists. This is important for later
                if "TEMP_FIELD" in fields:
                    arcpy.DeleteField_management(Feature, "TEMP_FIELD")
                else:
                    #if the field that is being looped through does not match the field type contained in the dictionary
                    if field.type != Field_type:
                        #If the field type listed in the dictionary is supposed to be text, but it is not with the input field
                        if Field_type == "TEXT" and field.type != "String":
                            print field.name + " is wrong field type"
                            #Calls the field length dictionary to find out how long all of the standard fields should be when made
                            Field_length = field_length_dict[str(field.name)]
                            print Field_length
                            print field.length
                            #Creates a list of the lengths of all of the values of the fields. This is used later
                            value_length_list = []
                            #Creates a modular cursor that changes the input field as a new field comes in
                            cursor = arcpy.da.UpdateCursor(Feature, field.name)
                            for row in cursor:
                                #If the row has a null value, it si changed to a empty space. This is important for later on
                                if row is None:
                                    row = ""
                                    cursor.updateRow(row)
                                else:
                                    #Sets a variable to the rows of the input field
                                    value = row[0]
                                    #print type(value)
                                    #print field.type
                                    #If the row is null, but the field type is numeric, it is changed to a zero
                                    if value is None and field.type in ('Double', 'Integer', 'Long'):
                                        #print value
                                        row[0] = int(0)
                                        cursor.updateRow(row)
                                    #This double checks that null values are caught
                                    elif value is None and field.type == 'Text':
                                        print value
                                        row[0] = ""
                                        cursor.updateRow(row)
                                    else:
                                        #If the row is an int or a float
                                        if type(value) in (int,float):
                                            #The length of the input row is found
                                            intstring = str(value)
                                            #and the length is appended to the already created list
                                            value_length_list.append(len(intstring))
                                        else:
                                            #if the row is text, the length of the row is appened to the list
                                            value_length_list.append(len(value))

                            #Finds the maximum length of the value lengths in the list
                            max_length = max(value_length_list)
                            print max_length
                            #If the length of the row is longer than what the standard field will hold
                            if max_length > Field_length and field.type == 'String':
                                print field.name + " in " + fc + " Will Not Fit In Standard"
                            else:
                                #The original field with the wrong type is changed to a dummy field with the name Temp
                                arcpy.AlterField_management(Feature, field.name, "TEMP_FIELD", "TEMP_FIELD")
                                #A new field with the correct name, type, and length is created
                                arcpy.AddField_management(Feature, field.name, Field_type, "", "", Field_length, field.name)
                                #The values of the old field are then put into the new field
                                arcpy.CalculateField_management(Feature, field.name, "!TEMP_FIELD!", "PYTHON_9.3")
                                #The old field with name Temp is then deleted.
                                arcpy.DeleteField_management(Feature, "TEMP_FIELD")
                        else:
                            if field.type != "String" and Field_type != "TEXT":
                                if field.type != "Double" and Field_type != "DOUBLE":
                                    print field.name + " has wrong field type but not text"
                                else:
                                    pass
                            else:
                                pass
                    else:
                        pass
            else:
                pass
