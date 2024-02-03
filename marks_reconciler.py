import openpyxl
from pathlib import Path
import re
import multiprocessing as mp
import concurrent.futures



def validate_marks_between_sheets(excel,sheet_1,sheet_2,reconcile_dict,queue=None):
    workbook = openpyxl.load_workbook(excel,read_only=True,data_only=True)
    student_name = " ".join(excel.stem.split(" ")[1:])
    sheet1 =workbook[sheet_1] 
    sheet2 =workbook[sheet_2]
    for sheet_1_cell, sheet_2_cell in reconcile_dict.items():
        if not sheet1[sheet_1_cell].value == sheet2[sheet_2_cell].value:
            queue.put(f"Error in the excel sheet of student {student_name} Error cells!!  {sheet_1}: {sheet_1_cell}, {sheet_2}: {sheet_2_cell}")
            # logger.error(f"Error in the excel sheet of student {student_name} Error cells!!  {sheet_1}: {sheet_1_cell}, {sheet_2}: {sheet_2_cell}")
    workbook.close()
            


def reconcile_sheets_marks(folder_name,sheet1,sheet2,reconcile_dict,logger):
    # iterate the folder to get the excel sheets
    queue = mp.Manager().Queue()
    main_dir = Path(folder_name)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for dir in main_dir.iterdir():
            for excel in dir.rglob("*.xlsx"):
                file_name = excel.name
                if re.match(r"\d+\s+[a-z A-Z]{5,40}.xlsx",file_name):
                    # validate_marks_between_sheets(excel,sheet1,sheet2,reconcile_dict,logger)
                        executor.submit(validate_marks_between_sheets, excel, sheet1, sheet2, reconcile_dict,queue)
                
    while not queue.empty():
        logger.error(queue.get())
                


    