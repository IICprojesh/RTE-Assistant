import os

def validate_file(fieldName,filePath):
    print(f"filePath: {filePath}")
    if os.path.isfile(filePath):
        return {f"error{fieldName}":False}
    else:
        return{f"error{fieldName}":f"The value in field Name {fieldName} should exists in your machine as a file"}


def validate_folder(fieldName,folderPath):
    if os.path.isdir(folderPath):
        return {f"error{fieldName}":False}
    else:
        return {f"error{fieldName}":f"The value in field Name {fieldName} should exists in your machine as a directory"}


def validate_integer(fieldName,value):
    if value.isdigit():
        return {f"error{fieldName}":False}
    else:
        return {f"error{fieldName}":f"The value in the field {fieldName} must be integer"}



def validator_engine(**kwargs):
    print("inside validator engine")
    print("kwargs",kwargs)
    errorsDict = {}
    for key,vals in kwargs.items():
        validator_function = vals[0]
        field_name = key
        field_value = vals[1]

        result = validator_function(field_name,field_value)
        if  not result[f"error{field_name}"] ==False:
            errorsDict.update(result)
            break
    return errorsDict
