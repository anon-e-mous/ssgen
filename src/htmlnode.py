from enum import Enum

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children} {self.props_to_html()})"

    def to_html(self):
        raise Exception("NotImplementedError")
    
    def props_to_html(self):
        if (self.props is None) or (not self.props):
            return ""
        else:
            props_string = ""
            for k, v in self.props.items():
                props_string += f' {k}="{v}"'
            return props_string