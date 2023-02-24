import openpyxl
from pathlib import Path
import re



def validate_marks_between_sheets(excel,sheet_1,sheet_2,reconcile_dict,logger):
    print(f"excel is : {excel}")
    workbook = openpyxl.load_workbook(excel,read_only=True,data_only=True)
    print(f"workbook: {workbook}")
    print(f"sheet_1 name: {sheet_1}")
    print(f"sheet_1 name: {sheet_2}")
    student_name = " ".join(excel.stem.split(" ")[1:])
    sheet1 =workbook[sheet_1] 
    sheet2 =workbook[sheet_2]
    print(f"sheet1: {sheet1}")
    print(f"sheet2: {sheet2}")
    print(f"reconcile_dict: {reconcile_dict}") 
    for sheet_1_cell, sheet_2_cell in reconcile_dict.items():
        print(f"sheet1[sheet_1_cell].value: {sheet1[sheet_1_cell].value}")
        print(f"sheet2[sheet_2_cell].value: {sheet2[sheet_2_cell].value}")
        if not sheet1[sheet_1_cell].value == sheet2[sheet_2_cell].value:
            logger.error(f"Error in the excel sheet of student {student_name} Error cells!!  {sheet_1}: {sheet_1_cell}, {sheet_2}: {sheet_2_cell}")
    workbook.close()
            


def reconcile_sheets_marks(folder_name,sheet1,sheet2,reconcile_dict,logger):
    # iterate the folder to get the excel sheets
    main_dir = Path(folder_name)
    for dir in main_dir.iterdir():
        for excel in dir.rglob("*.xlsx"):
            file_name = excel.name
            if re.match(r"\d+\s+[a-z A-Z]{5,20}.xlsx",file_name):
                validate_marks_between_sheets(excel,sheet1,sheet2,reconcile_dict,logger)
                


                


    