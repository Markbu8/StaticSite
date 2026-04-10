import os
import shutil

def copy_static(src,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        
    os.mkdir(dest)
    
    return file_recursion(src,dest)
    
def file_recursion(src,dest):
    
    file_folder_list = os.listdir(src)
    
    for f_or_f in file_folder_list:
        src_path = os.path.join(src,f_or_f)
        dest_path = os.path.join(dest,f_or_f)
        if os.path.isfile(src_path):
            shutil.copy(src_path,dest_path)
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            file_recursion(src_path,dest_path)