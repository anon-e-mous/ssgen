import os, shutil, sys

from textnode import TextType, TextNode
from blocknode import BlockType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from functions import *

def remove_directory_contents(path):
    files_to_delete = os.listdir(path)
    print("looking in ", path)
    if not files_to_delete:
        return
    for file in files_to_delete:
        if os.path.isdir(os.path.join(path, file)):
            remove_directory_contents(os.path.join(path, file))
            print("removing directory", file)
            os.rmdir(os.path.join(path, file))
        elif os.path.isfile(os.path.join(path, file)):
            print("removing file", file)
            os.remove(os.path.join(path, file))
        else:
            print("no idea what this is!")

def populate_directory_with_contents(source, target):
    files_to_copy = os.listdir(source)
    print("getting files in ", source)
    if not files_to_copy:
        return
    for file in files_to_copy:
        if os.path.isdir(os.path.join(source, file)):
            os.mkdir(os.path.join(target, file))
            print("dir created", os.path.join(target, file))
            populate_directory_with_contents(os.path.join(source, file), os.path.join(target, file))
            
        elif os.path.isfile(os.path.join(source, file)):
            shutil.copy(os.path.join(source, file), os.path.join(target, file))
            print("file", os.path.join(source, file), "copied to", os.path.join(target, file))
        else:
            print("no idea what this is!")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as infile:
        md = infile.read()
    title = extract_title(md)
    with open(template_path, "r") as usingfile:
        tp = usingfile.read()
    node = markdown_to_html_node(md)
    content = node.to_html()
    tp = tp.replace("{{ Title }}", title)
    tp = tp.replace("{{ Content }}", content)
    tp = tp.replace('href="/', f'href="{basepath}')
    tp = tp.replace('src="/', f'src="{basepath}')
    target_dirs = os.path.dirname(dest_path)
    if not os.path.exists(target_dirs):
        os.makedirs(target_dirs)
    with open(dest_path, "w") as outfile:
        outfile.write(tp)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files_in_dir = os.listdir(dir_path_content)
    if not files_in_dir:
        return
    else:
        for file in files_in_dir:
            print("file in list of files", file)
            if os.path.isdir(os.path.join(dir_path_content, file)):
                os.mkdir(os.path.join(dest_dir_path, file))
                generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), basepath)
            else:
                filepath, file_extension = os.path.splitext(os.path.join(dir_path_content, file))
                filename = os.path.basename(filepath)
                if file_extension == ".md":
                    filename += '.html'
                    generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, filename), basepath)

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    remove_directory_contents('docs')
    populate_directory_with_contents('static', 'docs')
    generate_pages_recursive('content', './template.html', 'docs', basepath)
    
    #generate_page("content/index.md", "./template.html", "public/index.html", basepath)
    #generate_page("content/blog/glorfindel/index.md", "./template.html", "public/blog/glorfindel/index.html", basepath)
    #generate_page("content/blog/tom/index.md", "./template.html", "public/blog/tom/index.html", basepath)
    #generate_page("content/blog/majesty/index.md", "./template.html", "public/blog/majesty/index.html", basepath)
    #generate_page("content/contact/index.md", "./template.html", "public/contact/index.html", basepath)

    #node = markdown_to_html_node("![JRR Tolkien sitting](/images/tolkien.png)")
    #print(node)
    #content = node.to_html()

if __name__ == "__main__":
    main()