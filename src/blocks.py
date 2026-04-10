import re
from enum import Enum
from htmlnode import *
from textnode import *
from copystatic import copy_static
import os

class BlockType (Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "u"
    ORDERED_LIST ="o"
    
def block_to_block_type(block):
    if ("# " == block[:2] or 
        "## " == block[:3] or 
        "### " == block[:4] or 
        "#### " == block[:5] or 
        "##### " == block[:6] or
        "###### "  == block[:7]):
        return BlockType.HEADING
    elif block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    elif block[:1] == ">" and not re.search(r"\n(?!>)",block[1:]):
        return BlockType.QUOTE
    elif block[:2] == "- " and not re.search(r"\n(?!- )",block[1:]):
        return BlockType.UNORDERED_LIST
    else:
        ordered_split = block.split("\n")
        ordered = True
        for i in range(0,len(ordered_split)):
            if ordered_split[i].startswith(f"{i+1}. ") is False:
                ordered = False
        if ordered:
            return BlockType.ORDERED_LIST
        
        return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def markdown_to_html_node(markdown):
    blocks =  markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = " ".join(line.strip() for line in block.split("\n"))
                html_nodes = text_to_htmlnodes(text)
                children_nodes.append(ParentNode("p",html_nodes))
            case BlockType.HEADING:
                heading_num_tag = create_heading_num_tag(block)
                text = block[heading_num_tag + 1:]
                html_nodes = text_to_htmlnodes(text)
                children_nodes.append(ParentNode(f"h{heading_num_tag}",html_nodes))
            case BlockType.CODE:
                children_nodes.append(ParentNode("pre",[LeafNode("code",block[4:-3])]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                stripped = [line.lstrip(">").strip() for line in lines]
                text = " ".join(stripped)
                html_nodes = text_to_htmlnodes(text)
                children_nodes.append(ParentNode("blockquote",html_nodes))
            case BlockType.UNORDERED_LIST:
                li_nodes = []
                for line in block.split("\n"):
                    item_text = line[2:]
                    item_html_nodes = [text_node_to_html_node(n) for n in text_to_textnodes(item_text)]
                    li_nodes.append(ParentNode("li", item_html_nodes))
                children_nodes.append(ParentNode("ul",li_nodes))
            case BlockType.ORDERED_LIST:
                li_nodes = []
                for line in block.split("\n"):
                    item_text = line.split(". ",1)[1]
                    item_html_nodes = [text_node_to_html_node(n) for n in text_to_textnodes(item_text)]
                    li_nodes.append(ParentNode("li", item_html_nodes))
                children_nodes.append(ParentNode("ol",li_nodes))
    return ParentNode("div",children_nodes)

def text_to_htmlnodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def create_heading_num_tag(block):
    for i in range(0,7):
        if block[i:i+1] != "#":
            return i
    raise Exception("too many # in heading")