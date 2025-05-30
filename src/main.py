import os
import shutil

from copystatic import recursive_copying
from generator import recursive_page_generation

dir_path_static = "./static"
dir_path_public = "./public"

dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    recursive_copying(dir_path_static, dir_path_public)

    print(f"Generating page from {dir_path_content} to {dir_path_public} using {template_path}.")
    recursive_page_generation(dir_path_content, template_path, dir_path_public)

    

main()
