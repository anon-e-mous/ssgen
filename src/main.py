import os, shutil

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generatting page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as infile:
        md = infile.read()
    title = extract_title(md)
    with open(template_path, "r") as usingfile:
        tp = usingfile.read()
    node = markdown_to_html_node(md)
    content = node.to_html()
    tp = tp.replace("{{ Title }}", title)
    tp = tp.replace("{{ Content }}", content)
    target_dirs = os.path.dirname(dest_path)
    #print(target_dirs)
    if not os.path.exists(target_dirs):
        os.makedirs(target_dirs)
    with open(dest_path, "w") as outfile:
        outfile.write(tp)


def main():

    remove_directory_contents('public')
    populate_directory_with_contents('static', 'public')

    generate_page("content/index.md", "./template.html", "public/index.html")
    generate_page("content/blog/glorfindel/index.md", "./template.html", "public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md", "./template.html", "public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md", "./template.html", "public/blog/majesty/index.html")
    generate_page("content/contact/index.md", "./template.html", "public/contact/index.html")

    #node = markdown_to_html_node("![JRR Tolkien sitting](/images/tolkien.png)")
    #print(node)
    #content = node.to_html()

if __name__ == "__main__":
    main()