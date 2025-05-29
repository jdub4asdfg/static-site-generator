import os
import re
from functions import markdown_to_html_nodes

def recursive_page_generation(dir_path_content, template_path, dest_dir_path):
    pass


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    index_content = get_content(from_path)
    template_content = get_content(template_path)
    html_string = markdown_to_html_nodes(index_content).to_html()
    title = extract_title(index_content)
    website_content = template_content.replace("{{ Title }}", title)
    website_content = website_content.replace("{{ Content }}", html_string)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as to_file:
        to_file.write(website_content)


def get_content(file_path):
    with open(file_path) as f:
        file_contents = f.read()
    return file_contents


def extract_title(markdown):
    title = re.findall(r"^# (.*)", markdown)[0].strip()
    if not title:
        raise Exception
    else:
        return title


