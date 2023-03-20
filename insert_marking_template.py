from pathlib import Path
import shutil
import os
import tempfile

def iterate_folder(folder_path, excel_file):

    file_name = excel_file.filename
    print(f"file name: {file_name}")
    temp_file_name = tempfile.NamedTemporaryFile(suffix=file_name,prefix="", delete=False)
    excel_file.save(temp_file_name.name)
    print(f"sucessfuly saved the file")
    

    path = Path(folder_path)


    for each in path.iterdir():
        if not each.is_file():
            copy_excel_sheet(temp_file_name.name,each)
        else:
            folder_name = create_folder(each)
            copy_excel_sheet(temp_file_name.name,folder_name)
    
    # deleting the temp excel file
    temp_file_name.close()
    os.remove(temp_file_name.name)

        
def copy_excel_sheet(temp_excel_sheet_path,folder):
    print("inside copy excel")

    excel_file_name = Path(temp_excel_sheet_path).name
    file_extension = os.path.splitext(temp_excel_sheet_path)[1]
    print(f"file_extension: {file_extension}")
    student_folder_info= Path(folder).name
    if not os.path.exists(f"{folder}/{student_folder_info}{file_extension}"):
    # extracting student name and student id

        student_infos = student_folder_info.split( )
        student_name = " ".join(student_infos[1:])

        print("before copying the excel file")
        shutil.copy(temp_excel_sheet_path,folder)
        print("after copying the excel file")

        # logic to rename the file to the student name and id
        shutil.move(f"{folder}/{excel_file_name}",f"{folder}/{student_folder_info}{file_extension}")
        print(f"sucessfully renamed excle file to student name")


    """
    code to insert student name and student id inside excel sheet file
    """
    
        

def create_folder(file):
    folder_location = Path(file).parent.absolute()
    student_info = Path(file).stem
    print(f"student_info: {student_info}")

    new_folder_name = Path(f"{folder_location}/{student_info}")
    new_folder_name.mkdir(parents=True, exist_ok=True)
    shutil.move(file,new_folder_name)
    return new_folder_name



    


        
       