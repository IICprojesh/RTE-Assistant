from flask import Flask, flash, render_template, request, redirect
import os
from read_files import WriteToExcel, ReadFromExcel
import json
from time import time
from flask_sse import sse
from pathlib import Path
import logging

from insert_marking_template import iterate_folder
from insert_student_marks import handle_insert_student_marks
from helper_function import extract_input_values_from_client_input
from marks_reconciler import reconcile_sheets_marks
from validators import validate_file, validate_folder,validate_integer, validator_engine



app = Flask(__name__)

app.secret_key = "a secret key"


# initilizating the flask ssh server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')



# initilize the logger

def initilize_logger(filename="no path provided"):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    logging.basicConfig(encoding ='utf-8',level=logging.ERROR,format='%(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    ch = logging.FileHandler(filename = f'{desktop}/{filename}.log',mode='w')
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger



@app.route("/", methods=['GET', 'POST'])
def home():
    error = None
    if request.method=="POST":
        sse.publish({"message":"true"},type='activateModal')
        excelFile = request.files["excel_file"]
        finalSheetName = request.form.get("final_sheet_name").strip()
        startDepth = request.form.get("start_depth").strip()
        endDepth = request.form.get("end_depth").strip()
        colStartRange = request.form.get("col_start_range").upper().strip()
        colEndRange = request.form.get("col_end_range").upper().strip()
        studentCol = request.form.get("student_col").upper().strip()
        studentFolder = request.form.get("student_folder").strip()
        studentSheetName = request.form.get("student_sheet_name").strip()


        student_marks_dict = extract_input_values_from_client_input(request.form) # this function extracts the form values and return a dictonary required for making student marks dictonary

        mergeExcelSheet = True if request.form.get("merge_pdf") else False
        isGroupCourseWork = True if request.form.get("is_group_coursework") else False
       
        
        # validating the input fields

        try:
            errors_info = validator_engine(studentFolder = (validate_folder,studentFolder),
                                            startDepth = (validate_integer,startDepth),
                                            endDepth = (validate_integer,endDepth),
                                             )
            
            print(f"errors info: {errors_info}")
            for key in errors_info:
                raise Exception(errors_info[key])

            print(f"mergeExcelSheet, {mergeExcelSheet}")
            
            # inatilzing a class for a write to excel file
            print("initilizing class now")
            write_excel = WriteToExcel(
                file_name=excelFile,
                sheet_name=finalSheetName,
                start_depth=int(startDepth),
                end_depth=int(endDepth),
                column_start_range= colStartRange,
                column_end_range=colEndRange,
                student_id_column=studentCol
                )

            
            print("initilizing ReadFromExcel")

            # inilatizing a class for a write to excel file
            read_student_directory = ReadFromExcel(
                folder_path=studentFolder,
                marks_dict=student_marks_dict,
                sheet_name=studentSheetName,
                excel_object=write_excel,
                merge_excel = mergeExcelSheet,
                sse = sse,
                isGroupCourseWork = isGroupCourseWork
            )

            init = time()

            read_student_directory.read_folder()

            print(f"Time taken to run write to excel is {time()-init}")

            flash(f"Marks has been sucessfully written in the excel file","success")

        except Exception as e:
            flash(str(e),"danger")
        finally:
            return redirect("/")    

    return render_template("index.html", error=error)
       



@app.route("/add_excel_sheet",methods = ["GET","POST"])
def add_excel_sheet():
    if request.method == "POST":
        print("inside excel sheet")
        sse.publish({"message":"loading"},type="activateLoader")
        folder_name = request.form.get("student_folder")
        excel_sheet = request.files["excel_file"]
        print(f"excel_sheet: {excel_sheet}")
        iterate_folder(folder_name,excel_sheet)
        return redirect("/add_excel_sheet")
    return render_template("add_excel_sheet.html")



@app.route("/insert_student_marks",methods = ["GET","POST"])
def insert_student_marks():
    if request.method=="POST":
        folder_name = request.form.get("foldername")
        marks_infos = json.loads(request.form.get("marks_infos"))

        print(f"folder_name: {folder_name}")
        print(f"marks_infos: {marks_infos}")
        handle_insert_student_marks(folder_name,marks_infos)
        return redirect("/insert_student_marks")

    return render_template("insert_student_marks.html")

@app.route("/reconcile_student_marks",methods = ["GET","POST"])
def reconcile_marks():
    if request.method == "POST":
        sse.publish({"message":"loading"},type="activateLoader")
        folder_name = request.form.get("student_folder")
        sheet_1 = request.form.get("sheet-1")
        sheet_2 = request.form.get("sheet-2")
        cell_values_dict = extract_input_values_from_client_input(request.form)
        print(f"folder_name: {folder_name}")
        print(f"sheet_1: {sheet_1}")
        print(f"sheet_2: {sheet_2}")
        print(f"cell_values_dict: {cell_values_dict}")
        logger = initilize_logger(filename = Path(folder_name).stem)  # initilize the logger
        reconcile_sheets_marks(folder_name,sheet_1,sheet_2,cell_values_dict,logger)


    return render_template("marks_reconcilation.html")


if __name__ == "__main__":
    app.run(debug=True)