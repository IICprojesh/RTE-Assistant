import os
from pathlib import Path
from win32com import client
from PyPDF2 import PdfMerger
import pythoncom




def merge_excel_sheet_to_pdf(student_folder_path,excel_file,pdf_file):
    print("merging excel sheet to pdf")
    pythoncom.CoInitialize()
    excel = client.Dispatch("Excel.Application")

    print(f"excel is: {excel}")
    path_to_pdf = f"{student_folder_path}/sample.pdf"
    # excel = client.Dispatch("Excel.Application")
    print(f"student_folder_path: {student_folder_path}")
    # print(f"excel_file: {excel_file}")
    # print(f"pdf_file: {pdf_file}")
    print(f"path_to_pdf: {path_to_pdf}")

    # creating a pdf file from a excel sheeet
   
    print(f"excel file: {excel_file}")
    # excel.Workbooks.Close(excel_file)
    sheets = excel.Workbooks.Open(excel_file)
    print(f"sheets: {sheets}")
    work_sheet = sheets.Worksheets["Result"]
    print(f"work_sheet: {work_sheet}")
    work_sheet.ExportAsFixedFormat(0, path_to_pdf)
    print(f"path_to_pdf: {path_to_pdf}")
    print(f"sucessfully created pdf from  excel file")
    sheets.Close()
    

    # merging that pdf sheet to the main pdf file
    print("inside pdf meager")
    
    pdf_merger = PdfMerger()
    print(f"pdf_merger: {pdf_merger}")
    pdf_merger.append(pdf_file,import_outline=False)
    pdf_merger.merge(1,path_to_pdf)

    with Path(pdf_file).open("wb") as output_file:
        pdf_merger.write(output_file)
        pdf_merger.close()
        print(f"sucessfully merged a pdf file {pdf_file}")

    os.remove(path_to_pdf)
    print(f"sucessfully deleted pdf file for student {pdf_file}")
    

