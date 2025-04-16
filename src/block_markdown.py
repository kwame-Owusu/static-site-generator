from textnode import TextNode, TextType
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
  stripped_line = markdown.lstrip()
  if stripped_line.startswith('#'):
    #count number of consecutive # symbols
    heading_level = 0
    for char in stripped_line:
      if char == '#':
        heading_level += 1
      else:
        break
    if heading_level > 0 and (len(stripped_line) > heading_level and stripped_line[heading_level] == ' '):
      return BlockType.HEADING


def markdown_to_blocks(markdown: str) -> list[str]:
  blocks = markdown.split("\n\n")
  filtered_blocks = []
  for block in blocks:
    if block == "":
      continue
    block = block.strip()
    filtered_blocks.append(block)
  return filtered_blocks

print(block_to_block_type('###### H6'))