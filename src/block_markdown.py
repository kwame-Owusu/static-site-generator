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
  if stripped_line.startswith('```') and stripped_line.endswith('```'):
    return BlockType.CODE
  if stripped_line.startswith('>'):
    return BlockType.QUOTE
  if stripped_line.startswith('- '):
    return BlockType.UNORDERED_LIST

  period_position = stripped_line.find('.')
  if period_position > 0:
    prefix_num = stripped_line[:period_position]
    if prefix_num.isdigit():
      if period_position + 1 < len(stripped_line) and stripped_line[period_position + 1] == ' ':
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

print(block_to_block_type('1. First Item'))