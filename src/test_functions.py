import unittest
from functions import (
    text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, 
    split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node,
    extract_title)
from textnode import TextNode, TextType
from blocknode import BlockType
from leafnode import LeafNode


class TestFunctions(unittest.TestCase):
    def test_text_node_to_html_node(self):
        """Check text node returns leaf node with correct text, tag and props both None"""
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = text_node_to_html_node(node)
        self.assertEqual(node2.value, "This is a text node")
        self.assertEqual(node2.tag, None)
        self.assertEqual(node2.props, None)

class TestFunctions2(unittest.TestCase):
    def test_text_node_to_html_node(self):
        """Check text node returns leaf node with correct text and tag, props None"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = text_node_to_html_node(node)
        self.assertEqual(node2.value, "This is a text node")
        self.assertEqual(node2.tag, "b")
        self.assertEqual(node2.props, None)

class TestFunctions3(unittest.TestCase):
    def test_text_node_to_html_node(self):
        """Check text node returns leaf node with correct text and tag, props None"""
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = text_node_to_html_node(node)
        self.assertEqual(node2.value, "This is a text node")
        self.assertEqual(node2.tag, "i")
        self.assertEqual(node2.props, None)

class TestFunctions4(unittest.TestCase):
    def test_text_node_to_html_node(self):
        """Check text node returns leaf node with correct text and tag, props None"""
        node = TextNode("This is my `test` code", TextType.CODE)
        node2 = text_node_to_html_node(node)
        self.assertEqual(node2.value, "This is my `test` code")
        self.assertEqual(node2.tag, "code")
        self.assertEqual(node2.props, None)

class TestFunctions5(unittest.TestCase):
    def test_text_node_to_html_node(self):
        """Check text node returns leaf node with correct text, tag and props"""
        node = TextNode("Click Me", TextType.LINK, "This is a test url")
        node2 = text_node_to_html_node(node)
        self.assertEqual(node2.value, "Click Me")
        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.props, {"href": "This is a test url"})

class TestFunctions6(unittest.TestCase):
    def test_text_node_to_html_node(self):
        """Check text node returns leaf node with correct text, tag and props"""
        node = TextNode("This is test alt text", TextType.IMAGE, "This is a test image path")
        node2 = text_node_to_html_node(node)
        self.assertEqual(node2.value, "")
        self.assertEqual(node2.tag, "img")
        self.assertEqual(node2.props, {"src": "This is a test image path", "alt": "This is test alt text"})

class TestFunctions7(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """Check list of text (markdown) nodes returns correct list of HTML nodes"""
        nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        new_nodes = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.TEXT), new_nodes)

class TestFunctions8(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """Check list of text (markdown) nodes returns correct list of HTML nodes"""
        nodes = [TextNode("This is text with no code block", TextType.TEXT)]
        new_nodes = [
        TextNode("This is text with no code block", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.TEXT), new_nodes)

class TestFunctions9(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """Check list of text (markdown) nodes returns correct list of HTML nodes"""
        nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        new_nodes = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded phrase", TextType.BOLD),
        TextNode(" in the middle", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.TEXT), new_nodes)

class TestFunctions10(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """Check list of text (markdown) nodes returns correct list of HTML nodes"""
        nodes = [TextNode("This is text with an *italic phrase* in the middle", TextType.TEXT)]
        new_nodes = [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic phrase", TextType.ITALIC),
        TextNode(" in the middle", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.TEXT), new_nodes)

class TestFunctions11(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """Check list of text (markdown) nodes returns correct list of HTML nodes"""
        nodes = [TextNode("This is text with an _italic phrase_ in the middle", TextType.TEXT)]
        new_nodes = [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic phrase", TextType.ITALIC),
        TextNode(" in the middle", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.TEXT), new_nodes)

class TestFunctions12(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        """Check list of text (markdown) nodes returns correct list of HTML nodes"""
        nodes = [TextNode("This is text with *two*, yes two, *italic phrases* in the middle", TextType.TEXT)]
        new_nodes = [
        TextNode("This is text with ", TextType.TEXT),
        TextNode("two", TextType.ITALIC),
        TextNode(", yes two, ", TextType.TEXT),
        TextNode("italic phrases", TextType.ITALIC),
        TextNode(" in the middle", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.TEXT), new_nodes)

class TestFunctions13(unittest.TestCase):
    def test_extract_markdown_images(self):
        """Check capture group tuple(s) of image alt text and path are correctly returned in a list"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_lst = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), extracted_lst)

class TestFunctions14(unittest.TestCase):
    def test_extract_markdown_links(self):
        """Check capture group tuple(s) of anchor text and url are correctly returned in a list"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_lst = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), extracted_lst)

class TestFunctions15(unittest.TestCase):
    def test_extract_markdown_links(self):
        """Check capture group tuple(s) of anchor text and url are correctly returned in a list"""
        text = "This is text with no links"
        extracted_lst = []
        self.assertEqual(extract_markdown_links(text), extracted_lst)

class TestFunctions16(unittest.TestCase):
    def test_extract_markdown_links(self):
        """Check capture group tuple(s) of anchor text and url are correctly returned in a list"""
        text = "This is text only before the link [to boot dev](https://www.boot.dev)"
        extracted_lst = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), extracted_lst)

class TestFunctions17(unittest.TestCase):
    def test_extract_markdown_links(self):
        """Check capture group tuple(s) of anchor text and url are correctly returned in a list"""
        text = "[to boot dev](https://www.boot.dev) and text only after the link"
        extracted_lst = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), extracted_lst)


class TestFunctions18(unittest.TestCase):
    def test_split_nodes_image(self):
        """Check text nodes containing alt text and image paths are correctly split and returned as a list of text and LINK nodes"""
        node = [TextNode(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT,)]
        new_nodes = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.TEXT),
        TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),]
        extracted_lst = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(split_nodes_image(node), new_nodes)

class TestFunctions19(unittest.TestCase):
    def test_split_nodes_link(self):
        """Check text nodes containing anchor text and urls are correctly split and returned as a list of text and LINK nodes"""
        node = [TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)]
        new_nodes = [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),]
        self.assertEqual(split_nodes_link(node), new_nodes)

class TestFunctions20(unittest.TestCase):
    def test_text_to_textnodes(self):
        """Check markdown-flavored text is correctly returned as a list of TextNode objects."""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),]
        self.assertEqual(text_to_textnodes(text), text_nodes)

class TestFunctions21(unittest.TestCase):
    def test_markdown_to_blocks(self):
        """Check markdown-flavored string (the document) is correctly returned as a list of 'block' strings."""
        md = "This is **bolded** paragraph\n\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n- This is a list\n- with items"
        received_blocks = markdown_to_blocks(md)
        blocks = ["This is **bolded** paragraph", "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", "- This is a list\n- with items"]
        self.assertEqual(received_blocks, blocks)

class TestFunctions22(unittest.TestCase):
    def test_markdown_to_blocks(self):
        """Check markdown-flavored string (the document) is correctly returned as a list of 'block' strings."""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        #received_blocks = markdown_to_blocks(md)
        blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(markdown_to_blocks(md), blocks)

class TestFunctions23(unittest.TestCase):
    def test_block_to_block_type(self):
        """Check a markdown block and return its BlockType"""
        block = ">This is a quote"
        received_type = block_to_block_type(block)
        type = BlockType.QUOTE
        self.assertEqual(received_type, type)

class TestFunctions24(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "```This is a code block\nOn more than one line```"
        received_type = block_to_block_type(block)
        type = BlockType.CODE
        self.assertEqual(received_type, type)

class TestFunctions25(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "- This is an unordered list\n- With two items"
        received_type = block_to_block_type(block)
        type = BlockType.UL
        self.assertEqual(received_type, type)

class TestFunctions26(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "3. This is an ordered list\n4. With two lines"
        received_type = block_to_block_type(block)
        type = BlockType.OL
        self.assertEqual(received_type, type)
        
class TestFunctions27(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "This is **bolded** paragraph"
        received_type = block_to_block_type(block)
        type = BlockType.PARA
        self.assertEqual(received_type, type)

class TestFunctions28(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "```This should not be a code block\n as there are no backticks at the end"
        received_type = block_to_block_type(block)
        type = BlockType.PARA
        self.assertEqual(received_type, type)

class TestFunctions29(unittest.TestCase):
    def test_markdown_to_html_node(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")

class TestFunctions30(unittest.TestCase):
    def test_markdown_to_html_node(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><code><pre>This is text that _should_ remain\nthe **same** even with inline stuff</pre></code></div>")

class TestFunctions31(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        heading = extract_title(markdown)
        self.assertEqual(heading, "Hello")

class TestFunctions32(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        heading = extract_title(markdown)
        self.assertEqual(heading, "Hello")

class TestFunctions33(unittest.TestCase):
    def test_extract_title(self):
        markdown = "No h1 in this text"
        with self.assertRaises(Exception):
            extract_title(markdown)

class TestFunctions34(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Tolkien Fan Club"
        heading = extract_title(markdown)
        self.assertEqual(heading, "Tolkien Fan Club")


if __name__ == "__main__":
    unittest.main()