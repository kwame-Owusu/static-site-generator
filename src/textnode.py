from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    """
    represents the various types of inline text that can exist in HTML and Markdown.
    """
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
    
  
    def __repr__(self) -> str:
        return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_by_delimiter(old_nodes: TextNode, delimiter: str, text_type:TextType) -> list[TextNode]:
    """
     create TextNodes from raw markdown strings
    """
    result = []
    
    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        text = old_node.text
        
        # Look for the first pair of delimiters
        left_delimiter = text.find(delimiter)
        # If no opening delimiter, keep the node as is
        if left_delimiter == -1:
            result.append(old_node)
            continue
            
        # Find matching closing delimiter
        right_delimiter = text.find(delimiter, left_delimiter + len(delimiter))
        # If no closing delimiter, that's an error in the markdown
        if right_delimiter == -1:
            raise Exception(f"No closing delimiter found for {delimiter}")
            
        # Now split into three parts:
        before_text = text[:left_delimiter]
        delimited_text = text[left_delimiter + len(delimiter):right_delimiter]
        after_text = text[right_delimiter + len(delimiter):]
        
        # Add nodes to result
        if before_text:
            result.append(TextNode(before_text, TextType.TEXT))
        result.append(TextNode(delimited_text, text_type))
        if after_text:
            result.append(TextNode(after_text, TextType.TEXT))
    
    return result 
node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_by_delimiter([node], "`", TextType.CODE)
print(new_nodes)