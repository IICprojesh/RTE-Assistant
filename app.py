from flask import Flask, flash, render_template, request, redirect, Response
import os
from read_files import WriteToExcel, ReadFromExcel
import json
from time import time
from flask_sse import sse
from pathlib import Path
import logging
import json

from insert_marking_template import iterate_folder
from insert_student_marks import handle_insert_student_marks
from helper_function import (extract_input_values_from_client_input, extract_values_from_ajax_request,
                            open_excel_file_sheet, find_student_excel_file,
                            generate_marks_dictonary)
from marks_reconciler import reconcile_sheets_marks
from validators import validate_folder,validate_integer, validator_engine



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.json.sort_keys = False

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


@app.route('/create_marks_dictonary',methods=['GET', 'POST'])
def create_marks_dictonary():
    if request.method == "POST":
        excelfile = request.files['excelFile']
        
        sheetname,startDepth,colStartRange,colEndRange,studentFolderName,studentMarkStartCell,studentMarkEndCell, studentSheetName  = extract_values_from_ajax_request(request.form)
        rte_excel_file = open_excel_file_sheet(excelfile)
        student_excel_file = find_student_excel_file(studentFolderName)
        rte_excel_sheet = rte_excel_file[sheetname]
        rte_excel_file
        student_excel_sheet = student_excel_file[studentSheetName]
        student_rte_churn, is_error = generate_marks_dictonary(rte_excel_sheet,student_excel_sheet,startDepth,colStartRange, colEndRange, studentMarkStartCell, studentMarkEndCell)

        if is_error:
            result = json.dumps({'result':student_rte_churn,'iserror':is_error})
        else:
            student_rte_churn = json.dumps(student_rte_churn,sort_keys=False)
            result = json.dumps({'result':student_rte_churn,'iserror':is_error})
            
        rte_excel_file.close()
        student_excel_file.close() 
        return Response(result)



 


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
            
            for key in errors_info:
                raise Exception(errors_info[key])

            
            # inatilzing a class for a write to excel file
            
            write_excel = WriteToExcel(
                file_name=excelFile,
                sheet_name=finalSheetName,
                start_depth=int(startDepth),
                end_depth=int(endDepth),
                column_start_range= colStartRange,
                column_end_range=colEndRange,
                student_id_column=studentCol
                )


            

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


            flash(f"Marks has been sucessfully written in the excel file","success")

        except Exception as e:
            flash(str(e),"danger")
        finally:
            return redirect("/")    

    return render_template("index.html", error=error)
       



@app.route("/add_excel_sheet",methods = ["GET","POST"])
def add_excel_sheet():
    if request.method == "POST":
        sse.publish({"message":"loading"},type="activateLoader")
        folder_name = request.form.get("student_folder")
        excel_sheet = request.files["excel_file"]
        iterate_folder(folder_name,excel_sheet)
        return redirect("/add_excel_sheet")
    return render_template("add_excel_sheet.html")



@app.route("/insert_student_marks",methods = ["GET","POST"])
def insert_student_marks():
    if request.method=="POST":
        folder_name = request.form.get("foldername")
        marks_infos = json.loads(request.form.get("marks_infos"))
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
        logger = initilize_logger(filename = Path(folder_name).stem)  # initilize the logger
        import time
        start = time.perf_counter()
        reconcile_sheets_marks(folder_name,sheet_1,sheet_2,cell_values_dict,logger)
        end = time.perf_counter()


    return render_template("marks_reconcilation.html")


if __name__ == "__main__":
    app.run(debug=True)