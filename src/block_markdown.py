from textnode import TextNode, TextType
import re




def markdown_to_blocks(markdown):
  markdown = markdown.strip()
  blocks = []
  splitted = markdown.split('\n\n')
  for line in splitted:
    if line.strip():
      blocks.append(line.strip())
  return blocks 

md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """

print(markdown_to_blocks(md))