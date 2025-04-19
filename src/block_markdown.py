from textnode import * 
from htmlnode import *
import re
from enum import Enum


class BlockType(Enum):
  PARAGRAPH = "paragraph" 
  HEADING = "heading" 
  CODE = "code" 
  QUOTE = "quote" 
  UNORDERED_LIST = "unordered_list" 
  ORDERED_LIST = "ordered_list" 

def block_to_block_type(markdown: str) -> BlockType:
  lines = markdown.split('\n')
  if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
     return BlockType.HEADING
  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
     return BlockType.CODE
  if markdown.startswith(">"):
      for line in lines:
          if not line.startswith(">"):
              return BlockType.PARAGRAPH
      return BlockType.QUOTE
  if markdown.startswith("- "):
      for line in lines:
          if not line.startswith("- "):
              return BlockType.PARAGRAPH
      return BlockType.UNORDERED_LIST
  if markdown.startswith("1. "):
      i = 1
      for line in lines:
          if not line.startswith(f"{i}. "):
              return BlockType.PARAGRAPH
          i += 1
      return BlockType.ORDERED_LIST
  return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
  blocks = markdown.split("\n\n")
  filtered_blocks = []
  for block in blocks:
    if block == "":
      continue
    block = block.strip()
    filtered_blocks.append(block)
  return filtered_blocks

def markdown_to_html_node(markdown: str) -> HTMLNode:
    def text_to_children(text):
        # This function should parse inline markdown (bold, italic, etc.)
        # and return a list of HTMLNode objects
        # For now, let's create a simple version that just returns plain text
        text_node = TextNode(text, TextType.TEXT)
        return [text_node_to_html_node(text_node)]
    
    # Create a parent div node to contain all blocks
    parent_node = HTMLNode("div", None)
    html_nodes = []  # List to collect all block nodes
    
    markdown_blocks = markdown_to_blocks(markdown)
    
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            node = HTMLNode("p", None)
            node.children = text_to_children(block)
            html_nodes.append(node)
            
        elif block_type == BlockType.HEADING:
            # Count leading # characters to determine heading level
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            if level > 6:  # HTML only supports h1-h6
                level = 6
            heading_text = block[level:].strip()  # Remove the # characters and spaces
            node = HTMLNode(f"h{level}", None)
            node.children = text_to_children(heading_text)
            html_nodes.append(node)
            
        elif block_type == BlockType.QUOTE:
            node = HTMLNode("blockquote", None)
            # Remove '> ' from the beginning of each line
            quote_text = "\n".join([line.strip()[2:] if line.strip().startswith("> ") else line.strip() for line in block.split("\n")])
            node.children = text_to_children(quote_text)
            html_nodes.append(node)
        elif block_type == BlockType.CODE:
          # For code blocks, wrap in pre>code and don't parse inline markdown
          pre_node = HTMLNode("pre", None)
          code_node = HTMLNode("code", None)
          
          # Strip the ``` markers from the beginning and end
          code_lines = block.strip().split("\n")
          if len(code_lines) > 2:  # If there are at least 3 lines (including the markers)
              code_text = "\n".join(code_lines[1:-1])  # Remove first and last lines (```)
          else:
              code_text = ""
          
          # Create a text node directly, don't process inline markdown
          text_node = TextNode(code_text, TextType.TEXT)
          code_html_node = text_node_to_html_node(text_node)
          
          code_node.children.append(code_html_node)
          pre_node.children.append(code_node)
          html_nodes.append(pre_node) 

        elif block_type == BlockType.UNORDERED_LIST:
            node = HTMLNode("ul", None)
            # Remove '> ' from the beginning of each line
            quote_text = "\n".join([line.strip()[2:] if line.strip().startswith("> ") else line.strip() for line in block.split("\n")])
            node.children = text_to_children(quote_text)
            html_nodes.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            node = HTMLNode("ol", None) 
            code_text = "" 
            node.children = text_to_children(code_text)
            html_nodes.append(node)