import unittest
from htmlnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!", None)
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_children_not_allowed(self):
        # LeafNode should not accept children parameter
        with self.assertRaises(TypeError):
            # Attempt to create a LeafNode with children
            LeafNode("p", "text", {}, ["child1", "child2"])
 
if __name__ == "__main__":
    unittest.main(verbosity=2)
    