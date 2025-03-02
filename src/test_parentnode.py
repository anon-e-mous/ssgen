import unittest

from leafnode import LeafNode
from parentnode import ParentNode

# This lets you see the whole error message without truncation
if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        """Check correct html string for parent node with 4 child nodes"""
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

class TestParentNode2(unittest.TestCase):
    def test_to_html(self):
        """Check correct html string for parent node with 4 child nodes including a link node with props"""
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b><a href="https://www.google.com">Click me!</a><i>italic text</i>Normal text</p>')

class TestParentNode3(unittest.TestCase):
    def test_to_html(self):
        """Check correct html string for parent node with 4 child nodes including a link node with no props"""
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("a", "Click me!", {}),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b><a>Click me!</a><i>italic text</i>Normal text</p>')

class TestParentNode4(unittest.TestCase):
    def test_to_html(self):
        """Check correct html string for parent node with 4 child nodes one being a parent with its own two children"""
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
                ParentNode("p", 
            [
                LeafNode("b", "Bold text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
            ],
        ),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b><a href="https://www.google.com">Click me!</a><p><b>Bold text</b><a href="https://www.google.com">Click me!</a></p>Normal text</p>')

class TestParentNode5(unittest.TestCase):
    def test_to_html(self):
        """Check correct html string for parent node with 1 child node"""
        node = ParentNode("div",
            [
                LeafNode("span", "child"),
            ],
        )
        self.assertEqual(node.to_html(), '<div><span>child</span></div>')


class TestParentNode6(unittest.TestCase):
    def test_to_html(self):
        """Check correct html string for parent node with a parent child node with one child"""
        node = ParentNode("div",
            [
                ParentNode("span", 
            [
                LeafNode("b", "grandchild"),
            ],
        ),
            ],
        )
        self.assertEqual(node.to_html(), '<div><span><b>grandchild</b></span></div>')

if __name__ == "__main__":
    unittest.main()
