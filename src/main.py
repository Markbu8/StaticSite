from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode,TextType,text_node_to_html_node,split_nodes_delimiter,extract_markdown_images
from copystatic import *
from pages import *

def main():
    copy_static("./static","./public")
    generate_pages_recursive("./content/","template.html","public/")
    
if __name__ == "__main__":
    main()