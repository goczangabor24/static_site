import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("Just normal text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_unbalanced_delimiter_raises_error(self):
        node = TextNode("This is **broken text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

if __name__ == '__main__':
    unittest.main()