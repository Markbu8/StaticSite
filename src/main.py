from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode,TextType,text_node_to_html_node,split_nodes_delimiter,extract_markdown_images
from copystatic import *
from pages import *
import sys

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    copy_static("./static","./docs")
    generate_pages_recursive(f"content/","template.html",base_path,"docs/")
    
if __name__ == "__main__":
    main()