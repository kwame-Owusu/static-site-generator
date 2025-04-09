from textnode import TextNode, TextType
import re

def split_nodes_by_delimiter(old_nodes: TextNode, delimiter: str, text_type:TextType) -> list[TextNode]:
    """
     create TextNodes from raw markdown strings
    """
    new_nodes = []
    for old_node in old_nodes:
        # If this node is not a TEXT type node, just add it to results unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Initialize a temporary list to store the split nodes from this text node
        split_nodes = []
        
        # Split the text by the delimiter
        # For example: "Text with `code` in it" split by "`" becomes ["Text with ", "code", " in it"]
        sections = old_node.text.split(delimiter)
        
        # Check if the markdown is valid - there should be an odd number of sections
        # If we have even number of sections, it means there's an opening delimiter with no closing one
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        # Process each section
        for i in range(len(sections)):
            # Skip empty sections
            if sections[i] == "":
                continue
                
            # Even-indexed sections (0, 2, 4...) are regular text
            # Odd-indexed sections (1, 3, 5...) are content between delimiters (special formatting)
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        
        # Add all the split nodes to our result list
        new_nodes.extend(split_nodes)
    
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    """
    takes raw markdown text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.
    """
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images 

def extract_markdown_links(text: str) -> list[tuple]:
    """
    extracts markdown links instead of images. It should return tuples of anchor text and URLs
    """
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

