
class HTMLNode():
    def __init__(self,tag="",value="",children=None,props=None):
        self.tag  = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        string = ""
        if self.props:
            for key,val in self.props.items():
                string += f' {key}="{val}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children:{self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props={}):
        super().__init__(tag,value,None,props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("No value")
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("No children")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children:{self.children}, {self.props})"