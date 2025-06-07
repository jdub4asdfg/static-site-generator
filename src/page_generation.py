import os
import re
from md_conversion_logic import markdown_to_html_nodes


def recursive_page_generation(dir_path_content, template_path, dest_dir_path, basepath):
    list_of_files = os.listdir(dir_path_content)
    for file in list_of_files:
        new_dir_path_content = os.path.join(dir_path_content, file)
        if os.path.isdir(new_dir_path_content):
            new_dest_dir_path = os.path.join(dest_dir_path, file)
            os.mkdir(new_dest_dir_path)
            recursive_page_generation(
                new_dir_path_content, template_path, new_dest_dir_path, basepath
            )
        elif os.path.isfile(new_dir_path_content):
            html_file_name = re.findall(r"^(.*)md", file)[0] + "html"
            new_dest_dir_path = os.path.join(dest_dir_path, html_file_name)
            generate_page(
                new_dir_path_content, template_path, new_dest_dir_path, basepath
            )


def generate_page(from_path, template_path, dest_path, basepath):
    index_content = get_content(from_path)
    template_content = get_content(template_path)
    html_string = markdown_to_html_nodes(index_content).to_html()
    title = extract_title(index_content)
    website_content = template_content.replace("{{ Title }}", title)
    website_content = website_content.replace("{{ Content }}", html_string)
    website_content = website_content.replace('href="/', f'href="{basepath}')
    website_content = website_content.replace('src="/', f'src="{basepath}')
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
