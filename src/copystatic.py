import os
import shutil


def recursive_copying(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    list_of_files = os.listdir(source_dir_path)
    for file in list_of_files:
        new_source_path = os.path.join(source_dir_path, file)
        new_dest_dir_path = os.path.join(dest_dir_path, file)
        if os.path.isdir(new_source_path):
            recursive_copying(new_source_path, new_dest_dir_path)
        elif os.path.isfile(new_source_path):
            shutil.copy(new_source_path, new_dest_dir_path)          
