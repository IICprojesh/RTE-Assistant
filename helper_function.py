import re

def extract_input_values_from_client_input(values):
    columnName_cellValue_dictonary = dict()

    _key = ""
    for key,value in values.items():
        # remove the additional space if any using strip
        
        if re.match(r"key\d+",key):
            value = value.strip()
            _key = value
        elif re.match(r"value\d+",key):
            value = value.strip()
            columnName_cellValue_dictonary[_key] = value
        
    print("result",columnName_cellValue_dictonary)
    return columnName_cellValue_dictonary


def find_excel_sheet(each):
    """
    find the excel file for the student folder and return it
    """
    for file in each.rglob("*.xlsx"):        
        return file


def find_pdf_file(each):
    """
    find the pdf file for the student folder and return it
    """
    for file in each.rglob("*.pdf"):
        return file


def iterate_student_folder(folder_path):
    pass
