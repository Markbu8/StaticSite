import os
from blocks import markdown_to_html_node

def extract_title(markdown):
    split = markdown.split("\n")
    for line in split:
        if line[:2] == "# " :
            return line[2:]
    raise Exception("no heading")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new_html = template.replace("{{ Title }}",title).replace("{{ Content }}",html_string)
    os.makedirs(os.path.dirname(dest_path),exist_ok=True)
    dest_file = open(dest_path,mode="w")
    dest_file.write(new_html) 
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    file_folder_list = os.listdir(dir_path_content)
    
    for f_or_f in file_folder_list:
        src_path = os.path.join(dir_path_content,f_or_f)
        dest_path = os.path.join(dest_dir_path,f_or_f)
        if os.path.isfile(src_path):
            if src_path[-3:] == ".md":
                generate_page(src_path,template_path,dest_path.replace(".md",".html"))
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path,template_path,dest_path)