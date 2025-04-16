import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a simple paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("   Just some text with leading spaces."), BlockType.PARAGRAPH)
        
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("   # Heading with leading space"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.HEADING)
        
    def test_invalid_heading(self):
        # No space after # symbols
        self.assertEqual(block_to_block_type("#Invalid heading"), BlockType.PARAGRAPH)
        # # symbol in the middle of text
        self.assertEqual(block_to_block_type("This is not a #heading"), BlockType.PARAGRAPH)
        
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```code block```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("   ```code with leading space```"), BlockType.CODE)
        
    def test_not_code_block(self):
        # Only opening code marker
        self.assertEqual(block_to_block_type("```code without closing"), BlockType.PARAGRAPH)
        # Only closing code marker
        self.assertEqual(block_to_block_type("code without opening```"), BlockType.PARAGRAPH)
        # Code markers with additional text
        self.assertEqual(block_to_block_type("```code``` extra text"), BlockType.PARAGRAPH)
        
    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("   > Quote with leading space"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">No space after >"), BlockType.QUOTE)
        
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("   - List item with leading space"), BlockType.UNORDERED_LIST)
        
    def test_not_unordered_list(self):
        # No space after -
        self.assertEqual(block_to_block_type("-Invalid list item"), BlockType.PARAGRAPH)
        # - in the middle of text
        self.assertEqual(block_to_block_type("This is not a - list item"), BlockType.PARAGRAPH)
        
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("42. Forty-second item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("   123. Item with leading space"), BlockType.ORDERED_LIST)
        
    def test_not_ordered_list(self):
        # No space after period
        self.assertEqual(block_to_block_type("1.Invalid list item"), BlockType.PARAGRAPH)
        # No number before period
        self.assertEqual(block_to_block_type(".Invalid list item"), BlockType.PARAGRAPH)
        # Text between number and period
        self.assertEqual(block_to_block_type("1text. Not a list item"), BlockType.PARAGRAPH)
        # Non-digit before period
        self.assertEqual(block_to_block_type("a. Not a numerical list item"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
