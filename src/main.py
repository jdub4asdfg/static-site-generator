import os
import sys
import shutil

from copystatic import recursive_copying
from generator import recursive_page_generation

dir_path_static = "./static"
dir_path_docs = "./docs"

dir_path_content = "./content"
template_path = "./template.html"
default_basepath = '/'

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    recursive_copying(dir_path_static, dir_path_docs)

    print(
        f"Generating page from {dir_path_content} to {dir_path_docs} using {template_path}."
    )
    recursive_page_generation(
        dir_path_content, template_path, dir_path_docs, basepath
    )


main()
