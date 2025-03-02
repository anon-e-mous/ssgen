from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise Exception(ValueError)

    def __eq__(self, other):
        if ((self.tag == other.tag) and
           (self.value == other.value) and
           (self.props == other.props)):
               return True
        else:
            return False

    def __repr__(self):
        return f'LeafNode("{self.tag}","{self.value}", "{self.props_to_html()}")'

    def to_html(self):
        if (self.value is None): #or (not self.value):
            raise ValueError
        else:
            if (self.tag is None) or (not self.tag):
                return self.value
            else:
                if self.props:
                    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
                else:
                    return f'<{self.tag}>{self.value}</{self.tag}>'