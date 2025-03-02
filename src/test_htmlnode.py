import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        """Test props_to_html returns an empty string if props left blank"""
        node = HTMLNode()
        props = node.props_to_html()
        self.assertEqual(props, "")

class TestHTMLNode2(unittest.TestCase):
    def test_props_to_html(self):
        """Test props_to_html returns an empty string if props set to blank"""
        node = HTMLNode(props=None)
        props = node.props_to_html()
        self.assertEqual(props, "")

class TestHTMLNode3(unittest.TestCase):
    def test_props_to_html(self):
        """Test props_to_html returns an empty string if props set to an empty string"""
        node = HTMLNode(props="")
        props = node.props_to_html()
        self.assertEqual(props, "")

class TestHTMLNode4(unittest.TestCase):
    def test_props_to_html(self):
        """Test props_to_html returns correct html for href and target properties"""
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        props = node.props_to_html()
        self.assertEqual(props, ' href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()
