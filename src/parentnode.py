from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Missing children")

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props_to_html()})"

    def to_html(self):
        if (self.tag is None) or (not self.tag):
            raise ValueError("Missing tag")
        if (self.children is None):
            raise ValueError("Missing children")
        
        html_strings = []

        for child in self.children:
            html_strings.append(child.to_html())

        html_string = "".join(html_strings)

        props_html = self.props_to_html()

        if props_html:
            return f"<{self.tag}{props_html}>{html_string}</{self.tag}>"
        
        return f"<{self.tag}>{html_string}</{self.tag}>"