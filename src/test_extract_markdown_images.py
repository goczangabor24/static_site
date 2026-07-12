import unittest
from extract_markdown_images import extract_markdown_images, extract_markdown_links
from split_nodes import TextNode, TextType, split_nodes_image, split_nodes_link, text_to_textnodes
import blocks

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is plain text"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
        
        matches = extract_markdown_links(
            "This is the first text [link](https://example.com) then the next text [link2](https://example2.com) and finally the last text."
        )
        self.assertListEqual([("link", "https://example.com"), ("link2", "https://example2.com")], matches)

        matches = extract_markdown_links(
            "Here is an ![image](https://example.com/pic.png) and a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
        
        matches = extract_markdown_links(
            "[first link](https://example.com/start) then some text with an ![image](https://example.com/pic.png) and another [link](https://example.com/end)![another image](https://example.com/pic2.png)[back to back link](https://example.com/final)"
        )
        self.assertListEqual([("first link", "https://example.com/start"), ("link", "https://example.com/end"), ("back to back link", "https://example.com/final")], matches)

        matches = extract_markdown_images(
            "[first link](https://example.com/start) then some text with an ![image](https://example.com/pic.png) and another [link](https://example.com/end)![another image](https://example.com/pic2.png)[back to back link](https://example.com/final)"
        )
        self.assertListEqual([("image", "https://example.com/pic.png"), ("another image", "https://example.com/pic2.png")], matches)

class TestSplitNodes(unittest.TestCase):
    def test_split_image(self):
        matches = split_nodes_image(
            [TextNode("This is just plain text with no images", TextType.TEXT)]
        )
        self.assertListEqual([TextNode("This is just plain text with no images", TextType.TEXT)], matches)

        matches = split_nodes_image(
            [TextNode("![image](https://example.com/png) This is the rest of the text.", TextType.TEXT),
             TextNode("This is some text then only an image ![image](https://example.com/png)", TextType.TEXT),
             TextNode("This is text before ![image](https://example.com/png) this is text after.", TextType.TEXT),
             TextNode("This is the first text ![image](https://example.com/png) then the next text ![image2](https://example.com/png2) and finally the last text.", TextType.TEXT)]
        )
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/png"), TextNode(" This is the rest of the text.", TextType.TEXT),
                TextNode("This is some text then only an image ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://example.com/png"),
                TextNode("This is text before ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://example.com/png"), TextNode(" this is text after.", TextType.TEXT),
                TextNode("This is the first text ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://example.com/png"), TextNode(" then the next text ", TextType.TEXT), TextNode("image2", TextType.IMAGE, "https://example.com/png2"), TextNode(" and finally the last text.", TextType.TEXT) 
            ], matches
        )

    def test_split_nodes_link(self):
        matches = split_nodes_link(
            [
                TextNode("This is plain text", TextType.TEXT),
                TextNode("This is some text then only a link [link](https://example.com)", TextType.TEXT),
                TextNode("This is text before [link](https://example.com) this is text after.", TextType.TEXT),
                TextNode("This is the first text [link](https://example.com) then the next text [link2](https://example2.com) and finally the last text.", TextType.TEXT)
            ]
        )
        self.assertListEqual(
            [
                TextNode("This is plain text", TextType.TEXT),
                TextNode("This is some text then only a link ", TextType.TEXT), TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("This is text before ", TextType.TEXT), TextNode("link", TextType.LINK, "https://example.com"), TextNode(" this is text after.", TextType.TEXT),
                TextNode("This is the first text ", TextType.TEXT), TextNode("link", TextType.LINK, "https://example.com"), TextNode(" then the next text ", TextType.TEXT), TextNode("link2", TextType.LINK, "https://example2.com"), TextNode(" and finally the last text.", TextType.TEXT)
            ], matches
        )

class TestTextNodesConverter(unittest.TestCase):
    def test_text_to_testnodes(self):
        matches = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ], matches
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        node = blocks.markdown_to_html_node(
            """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        )
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        matches = blocks.markdown_to_blocks(
            """
This is **bolded** paragraph   

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
            """
        )
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ], matches
        )