import unittest
from htmlnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "hello, world!")
        self.assertEqual(node.to_html(), "<p>hello, world!</p>")
   
    def test_no_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_no_tag(self):
        node = LeafNode(value="hello world i love programming")
        expected = "hello world i love programming"
        self.assertEqual(node.to_html(), expected)

    def test_children_not_allowed(self):
        # LeafNode should not accept children parameter
        with self.assertRaises(TypeError):
            # Attempt to create a LeafNode with children
            LeafNode("p", "text", {}, ["child1", "child2"])
 
if __name__ == "__main__":
    unittest.main(verbosity=2)
    