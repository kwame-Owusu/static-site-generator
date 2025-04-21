import unittest
from block_markdown import *
from main import extract_title
import os
import sys

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
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
 
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def setUp(self):
        # Create test files before each test
        self.create_test_files()
    
    def create_test_files(self):
        # Create test files with different content
        with open("test_basic_header.md", "w") as f:
            f.write("# This is a title\nSome content\n## Subtitle")
        
        with open("test_no_space_header.md", "w") as f:
            f.write("#Tight title\nSome content")
        
        with open("test_multiple_headers.md", "w") as f:
            f.write("Some initial content\n# First Header\nMore content\n# Second Header")
        
        with open("test_different_levels.md", "w") as f:
            f.write("## Second level\n# First level\n### Third level")
        
        with open("test_no_header.md", "w") as f:
            f.write("No header here\nJust some content\nWithout any markdown headers")
        
        with open("test_empty.md", "w") as f:
            f.write("")
    
    def tearDown(self):
        # Clean up test files after each test
        import os
        test_files = [
            "test_basic_header.md",
            "test_no_space_header.md",
            "test_multiple_headers.md",
            "test_different_levels.md",
            "test_no_header.md",
            "test_empty.md"
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_extract_title_with_header(self):
        result = extract_title("test_basic_header.md")
        self.assertEqual(result, "This is a title")
    
    def test_extract_title_with_header_no_space(self):
        result = extract_title("test_no_space_header.md")
        self.assertEqual(result, "Tight title")
    
    def test_extract_title_with_multiple_headers(self):
        result = extract_title("test_multiple_headers.md")
        self.assertEqual(result, "First Header")
    
    def test_extract_title_with_multiple_hash_levels(self):
        result = extract_title("test_different_levels.md")
        self.assertEqual(result, "Second level")
    
    def test_extract_title_no_header(self):
        with self.assertRaises(Exception) as context:
            extract_title("test_no_header.md")
        
        self.assertEqual(str(context.exception), "No header found in markdown file")
    
    def test_extract_title_empty_file(self):
        with self.assertRaises(Exception) as context:
            extract_title("test_empty.md")
        
        self.assertEqual(str(context.exception), "No header found in markdown file")
    

if __name__ == "__main__":
    unittest.main()
