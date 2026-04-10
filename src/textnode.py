from enum import Enum
from htmlnode import LeafNode

import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "images"
    
class TextNode():
    def __init__(self,text="",text_type="",url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text,None)
        case TextType.BOLD:
            return LeafNode("b",text_node.text,None)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text,None)
        case TextType.CODE:
            return LeafNode("code",text_node.text,None)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in TextType:
        raise Exception("text_type not in TextType")
    new_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_list.append(node)
            continue
        split_texts = node.text.split(delimiter)
        if len(split_texts)%2 == 0:
            raise Exception("closing delimiter not found")
        for i in range(0,len(split_texts)):
            if split_texts[i] == "":
                continue
            if i % 2 == 0:
                new_list.append(TextNode(split_texts[i],TextType.TEXT))
            else:
                new_list.append(TextNode(split_texts[i],text_type))
    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)

def split_nodes_image(old_nodes):
    return split_nodes(old_nodes,True)

def split_nodes_link(old_nodes):
    return split_nodes(old_nodes,False)

def split_nodes(old_nodes,is_image):
    prefix = ""
    if is_image:
        prefix = "!"
    new_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_list.append(node)
            continue
        
        extracted_images = extract_markdown_images(node.text) if is_image else extract_markdown_links(node.text)
        
        if len(extracted_images) == 0:
            new_list.append(node)
            continue
        
        split_texts = ["",node.text]
        
        for extracted_image in extracted_images:
            if extracted_image[0] == "" or extracted_image[1] == "":
                continue
            split_texts = split_texts[1].split(f"{prefix}[{extracted_image[0]}]({extracted_image[1]})", 1)
            if split_texts[0] != "":
                new_list.append(
                    TextNode(split_texts[0],TextType.TEXT)
                )
            new_list.append(
                TextNode(
                    extracted_image[0],
                    TextType.IMAGE if is_image else TextType.LINK,
                    extracted_image[1]
                )
            )
        if split_texts[1] != "":
            new_list.append(
                TextNode(split_texts[1],TextType.TEXT)
            )
    return new_list

def text_to_textnodes(text):
    node_list = [TextNode(text,TextType.TEXT)]
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list,"**",TextType.BOLD)
    node_list = split_nodes_delimiter(node_list,"_",TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list,"`",TextType.CODE)
    return node_list