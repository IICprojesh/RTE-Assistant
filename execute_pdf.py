from pathlib import Path
from helper_function import find_excel_sheet, find_pdf_file
import os
import pythoncom
from PyPDF2 import PdfFileMerger
from win32com import client
import shutil


def inilize_wincom32():
    return client.Dispatch("Excel.Application",pythoncom.CoInitialize())


def merge_temp_to_main_pdf(main_pdf, temp_pdf):

# Create a PdfFileMerger object
    merger = PdfFileMerger()

    # Open the existing PDF
    existing_pdf = open(main_pdf, 'rb')

    # Open the PDF to be merged
    pdf_to_merge = open(temp_pdf, 'rb')

    # Add the existing PDF to the merger
    merger.append(existing_pdf)

    # Merge the PDF to be merged after page 1
    merger.merge(1, pdf_to_merge)

    # Write the merged PDF to a new file
    merged_output = open(main_pdf, 'wb')
    merger.write(merged_output)

    # Close the input and output files
    existing_pdf.close()
    pdf_to_merge.close()
    merged_output.close()

    # delete the temp_pdf
    os.remove(temp_pdf)



def create_pdf_of_sheet(excel,excel_file, sheet_name, orientation, papersize):
    workbook = excel.Workbooks.Open(excel_file)
    try:
        work_sheet = workbook.Worksheets[sheet_name]

        print("inside orientation paper size", orientation)
        print("inside papersize paper size", papersize)

        work_sheet.PageSetup.Orientation = orientation
        work_sheet.PageSetup.PaperSize = papersize

        print("parent folder name",excel_file.parent)

        temp_pdf_file_path = os.path.join((excel_file.parent),"demo.pdf")
        work_sheet.ExportAsFixedFormat(0, temp_pdf_file_path)

        workbook.Saved = True
        workbook.Close()
        excel.Quit()
        return temp_pdf_file_path
    except Exception as e:
        print(f"error has occured: {e}")
  




def handler_pdf(path, sheet_name, orientation, papersize):
    parent_path = Path(rf"{path}")
    excel = inilize_wincom32()
    for dir in parent_path.iterdir():
        
        excel_file = find_excel_sheet(dir)
        pdf_file = find_pdf_file(dir)

        if excel_file:
            temp_pdf_file = create_pdf_of_sheet(excel,excel_file,sheet_name,orientation,papersize)
        if pdf_file:
            merge_temp_to_main_pdf(pdf_file, temp_pdf_file)
     






