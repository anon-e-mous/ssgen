import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        """Checks correct html returned for a paragraph tag"""
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

class TestLeafNode2(unittest.TestCase):
    def test_to_html(self):
        """Checks correct html returned for a link tag with anchor text and href prop"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestLeafNode3(unittest.TestCase):
    def test_to_html(self):
        """Checks ValueError raised if no value"""
        node = LeafNode("a", "", {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()

class TestLeafNode4(unittest.TestCase):
    def test_to_html(self):
        """Checks raw text returned if empty string for tag"""
        node = LeafNode("", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "This is a paragraph of text.")

class TestLeafNode5(unittest.TestCase):
    def test_to_html(self):
        """Checks raw text returned if tag is None"""
        node = LeafNode(None, "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "This is a paragraph of text.")


if __name__ == "__main__":
    unittest.main()
