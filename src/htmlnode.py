

class HTMLNode():
    """
    represents a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents).
    It can be block level or inline, and is designed to only output HTML.

    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)\n
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)\n
    children - A list of HTMLNode objects representing the children of this node\n
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

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
    def __init__(self, tag: str = None ,value: str = None, props: dict[str, str] = None):
        super().__init__(tag, value, props,)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag == None:
            return f"{self.value}"

        return f"<{self.tag}>{self.value}</{self.tag}>"