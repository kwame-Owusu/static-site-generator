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

print(block_to_block_type('hello world ```coding``` dsad'))