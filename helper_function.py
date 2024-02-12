import re
from itertools import repeat
from difflib import get_close_matches
import openpyxl
from pathlib import Path
import re



def open_excel_file_sheet(excel_file, data_only=False, read_only=False):
    wb = openpyxl.load_workbook(excel_file,data_only=data_only,read_only=read_only)
    return wb



def find_student_excel_file(folder_name):
    path = Path(rf'{folder_name}')
    for p in path.iterdir():
        for file in p.rglob("*.xlsx"):
            if re.match(r"\d+\s+[a-z A-Z. ()]+.xlsx",file.name):
                wb = open_excel_file_sheet(excel_file=file,data_only=True, read_only=True)
                return wb

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

def range_char(asci_value,start_depth):
        
    return f"{chr(asci_value)}{start_depth}"
       



def arrange_order_on_similarities_between_rte_sheet_and_student_sheet(rte_dictonary,student_dictonary):
    student_rte_churn = dict()
    is_error = False
    try:
        for key in rte_dictonary:
            closest_value = get_close_matches(key, student_dictonary, n=1,cutoff=0.4)
            student_rte_churn[key] = student_dictonary[closest_value[0]]
    except Exception as e:
        is_error=True
        student_rte_churn="Error in the RTE sheet and Student Sheet"
    
    return student_rte_churn, is_error



def extract_field_name_and_mark_cell_value_from_student_sheet(sheet, start_row, end_row):
    marks_cell = chr(ord(start_row[0])+2)
    student_marks_dictonary = dict()
    is_error = False
    try:
        for cell_num in range(int(start_row[1:]),int(end_row[1:])+1):
            row_index_name = sheet[f"{start_row[0]}{cell_num}"].value.strip()
            print(f"row_index_name: {row_index_name}")
            if re.match('^\d[\.\s]+\w+$',row_index_name):
                row_index_name = " ".join(row_index_name.split('.')[1:]).strip()

            print(f"sheet_column_name: {row_index_name}")
            student_marks_dictonary[row_index_name] = f"{marks_cell}{cell_num}"
    except Exception as e:
        is_error = True
        student_marks_dictonary = "Error in the cell range provided for Student Sheet"
    
    return student_marks_dictonary, is_error



def generate_marks_dictonary(rte_excel_sheet,student_excel_file, start_depth,start_range, end_range, student_sheet_start_range, student_sheet_end_range):
    rte_sheet_cell_arrays = list(map(range_char,range(ord(start_range), ord(end_range)+1), repeat(start_depth-1)))
    rte_sheet_dictonary = {rte_excel_sheet[cell].value.split('(')[0].strip():cell for cell in rte_sheet_cell_arrays} 
    print(f"rte_sheet_dictonary: {rte_sheet_dictonary}")   
    student_sheet_dictonary, iserror = extract_field_name_and_mark_cell_value_from_student_sheet(student_excel_file, student_sheet_start_range, student_sheet_end_range)
    print(f"student_sheet_dictonary: {student_sheet_dictonary}")
    if iserror:
        return student_sheet_dictonary,iserror
    
    return arrange_order_on_similarities_between_rte_sheet_and_student_sheet(rte_sheet_dictonary, student_sheet_dictonary)


def extract_values_from_ajax_request(dict):
    sheetname = dict.get('sheetName')
    colStartRange = dict.get('colStartRange')
    colEndRange = dict.get('colEndRange')
    studentFolderName = dict.get('studentFolderName')
    studentMarkStartCell = dict.get('studentMarkStartCell')
    studentMarkEndCell = dict.get('studentMarkEndCell') 
    studentSheetName = dict.get('studentSheetName')
    startDepth = int(dict.get('startDepth'))
    return sheetname,startDepth, colStartRange, colEndRange,studentFolderName,studentMarkStartCell,studentMarkEndCell,studentSheetName  




