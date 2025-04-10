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


def split_nodes_image(old_nodes: TextNode) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: TextNode) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    """
    function that can convert a raw string of markdown-flavored text into a list of TextNode objects.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_by_delimiter(nodes,'`', TextType.CODE)   
    nodes = split_nodes_by_delimiter(nodes,'**', TextType.BOLD)   
    nodes = split_nodes_by_delimiter(nodes,'_', TextType.ITALIC)   
    nodes = split_nodes_image(nodes)  
    nodes = split_nodes_link(nodes)   
    return nodes 


test_string  = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
print(text_to_textnodes(test_string))