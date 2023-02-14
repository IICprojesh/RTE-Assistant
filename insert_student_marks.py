from pathlib import Path
from helper_function import find_excel_sheet, find_pdf_file

from openpyxl import load_workbook
from pathlib import Path
import numpy as np
import random


def add_marks_on_student_sheet(excel_file, marks_info):
    print("inside add_marks_on_student_sheet")
    print(f"excel_file: {excel_file}")
    workbook = load_workbook(excel_file)
    sheet = workbook["Grading Sheet"]
    print(f"marks_info: {marks_info}")
    for key, value in marks_info.items():
        print(f"value is: {value}")
        print(f"Changing the marks of cell: {key}")
        """
        it creates a marks value from a given lists randomly within a given range having spacing of 0.5
        """

        marks_value = random.choice(np.arange(value[0],value[1]+1,0.5)) 
        print(f"marks_value: {marks_value}")

        sheet[key] = marks_value

    workbook.save(excel_file)
    workbook.close()

    

def handle_insert_student_marks(folder_name,marks_info):
    for path in Path(folder_name).iterdir():
        excel_file = find_excel_sheet(path)
        add_marks_on_student_sheet(excel_file,marks_info)


        
