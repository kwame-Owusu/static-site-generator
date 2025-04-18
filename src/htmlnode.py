
class HTMLNode():
    """
    represents a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents).
    It can be block level or inline, and is designed to only output HTML.

    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)\n
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)\n
    children - A list of HTMLNode objects representing the children of this node\n
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, 
    ka link (<a> tag) might have {"href": "https://www.google.com"}

    """
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None) -> None: 
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> Exception:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> None:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag!r}, {self.value!r}, children: {self.children!r}, {self.props!r})"


class LeafNode(HTMLNode):
    """
    A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.\n 
    For example, a simple p tag with some text inside of it:\n
    p This is a paragraph of text./p
    """
    def __init__(self, tag: str,value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props,)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    """
    ParentNode class will handle the nesting of HTML nodes inside of one another.\n 
    Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
    """
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: a tag is needed")
        
        if self.children ==  None:
            raise ValueError("invalid HTML: children are needed")

        children_html = ""
        for child in self.children:
            children_html += child.to_html() 
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"