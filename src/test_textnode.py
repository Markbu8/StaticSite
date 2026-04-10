import unittest

from textnode import *
from blocks import *
from copystatic import *
from pages import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/cat.png", "alt": "a cat"})

    def test_invalid_type(self):
        node = TextNode("oops", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
            
class TestSplit_nodes_delimiter(unittest.TestCase):
    def test_normal_case(self):
        node = TextNode("This `code block` is text with a", TextType.TEXT)
        node1 = TextNode("This is text with a `code block`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node,node1], "`", TextType.CODE),[
            TextNode("This ", TextType.TEXT, None), 
            TextNode("code block", TextType.CODE, None), 
            TextNode(" is text with a", TextType.TEXT, None), 
            TextNode("This is text with a ", TextType.TEXT, None), 
            TextNode("code block", TextType.CODE, None)])

    def test_not_text_type(self):
        node = TextNode("This `code block` is text with a", TextType.BOLD)
        node1 = TextNode("This is text with a `code block`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node,node1], "`", TextType.CODE),[
            TextNode("This `code block` is text with a", TextType.BOLD, None), 
            TextNode("This is text with a ", TextType.TEXT, None), 
            TextNode("code block",  TextType.CODE, None)])

    def test_delimit_at_start(self):
        node = TextNode("`code block` is text with a", TextType.TEXT)
        node1 = TextNode("`code block`This is text with a", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node,node1], "`", TextType.CODE),[
            TextNode("code block", TextType.CODE, None), 
            TextNode(" is text with a", TextType.TEXT, None), 
            TextNode("code block", TextType.CODE, None), 
            TextNode("This is text with a", TextType.TEXT, None)])
    
    def test_delimit_at_end(self):
        node = TextNode("is text with a`code block`", TextType.TEXT)
        node1 = TextNode("This is text with a`code block`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node,node1], "`", TextType.CODE),[
            TextNode("is text with a", TextType.TEXT, None), 
            TextNode("code block", TextType.CODE, None), 
            TextNode("This is text with a", TextType.TEXT, None), 
            TextNode("code block", TextType.CODE, None)])
    
    def test_empty_string_between(self):
        node = TextNode("is text with a`code block1``code block2`", TextType.TEXT)
        node1 = TextNode("`code block3``code block4`This is text with a", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node,node1], "`", TextType.CODE),[
            TextNode("is text with a", TextType.TEXT, None), 
            TextNode("code block1", TextType.CODE, None), 
            TextNode("code block2", TextType.CODE, None), 
            TextNode("code block3", TextType.CODE, None), 
            TextNode("code block4", TextType.CODE, None), 
            TextNode("This is text with a", TextType.TEXT, None)])
        
class Testextract_markdown(unittest.TestCase):
    
    def test_normal_case_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a [rioll](https://i.iIh.gif) and [obi wa](https://i.imgur.com/fg)"
        self.assertEqual(extract_markdown_images(text),[
            ("rick roll","https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")
            ])
        
    def test_normal_case_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a [rioll](https://i.iIh.gif) and [obi wa](https://i.imgur.com/fg)"
        self.assertEqual(extract_markdown_links(text),[
            ("rioll","https://i.iIh.gif"),
            ("obi wa","https://i.imgur.com/fg")
            ])
        
    def test_normal_case_images_none(self):
        text = "This is text with a ![]() and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a [rioll](https://i.iIh.gif) and [obi wa](https://i.imgur.com/fg)"
        self.assertEqual(extract_markdown_images(text),[
            ("",""),
            ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")
            ])
        
    def test_normal_case_images_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a [rioll](https://i.iIh.gif) and []()"
        self.assertEqual(extract_markdown_links(text),[
            ("rioll","https://i.iIh.gif"),
            ("","")
            ])
        
class Testsplit_nodes(unittest.TestCase):
    def test_base_test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is text with anssssss",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" This is text with anssssss", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_images_links_too(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is text with anssssss",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" This is text with anssssss", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another This is text with anssssss",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another This is text with anssssss", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_images_exlaim_in_text(self):
        node = TextNode(
            "This is text wit!!!h an ![image](https://i.imgur.com/zjjcJKZ.png) and a!!!nother ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text wit!!!h an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a!!!nother ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_base_test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_link_text_after(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) This is text with anssssss",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" This is text with anssssss", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_link_images_too(self):
        node = TextNode(
            "This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) This is text with anssssss",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" This is text with anssssss", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_link_no_links(self):
        node = TextNode(
            "This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and another This is text with anssssss",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and another This is text with anssssss", TextType.TEXT),
            ],
            new_nodes,
        )
        
class Testtext_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
            new_nodes,
        )
        
class Testmarkdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class Testmarkdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
class Testextract_title(unittest.TestCase):
    def test_extract_title(self):
        md = """
## line 12
line 1
# line 4
"""
        self.assertEqual(
            extract_title(md),
            "line 4",
        )
        
    def test_extract_title_error(self):
        md = """
## line 12
line 1
line 4
"""
        with self.assertRaises(Exception):
            extract_title(md)
        
if __name__ == "__main__":
    unittest.main()