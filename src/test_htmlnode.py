import unittest
from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "Hello", None, None)
        expected = "HTMLNode('p', 'Hello', children: None, None)"
        self.assertEqual(repr(node), expected)

    def test_not_equal_nodes(self):
        node1 = HTMLNode("p", "Hello")
        node2 = HTMLNode("div", "Hello")
        self.assertNotEqual(node1, node2) 
    
    def test_props_to_html(self):
        node_props = {"href": "https://www.google.com", "target": "_blank"}
        node1 = HTMLNode("p", "Hello", None, props=node_props)
        
        result = node1.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(result, expected)
   

if __name__ == "__main__":
    unittest.main()
    