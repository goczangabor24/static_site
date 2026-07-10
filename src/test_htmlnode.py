import unittest
from htmlnode import HTMLNode, ParentNode
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag='div', value='This is a text node', props={'class': 'text-node'})
        node2 = HTMLNode(tag='div', value='This is a text node', props={'class': 'text-node'})
        node3 = HTMLNode(tag='span', value='This is the 3rd text node', props={'class': 'text-node'})

        result = node.props_to_html()
        result2 = node2.props_to_html()
        result3 = node3.props_to_html()
        self.assertEqual(result, ' class="text-node"')
        self.assertEqual(result2, ' class="text-node"')
        self.assertEqual(result3, ' class="text-node"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode(tag='p', value='Hello, world!')
        node2 = LeafNode(tag='a', value='Click here', props={'href': 'https://example.com'})
        node3 = LeafNode(tag=None, value="Just some text without a tag")
        node4 = LeafNode(tag='b', value='Bold text', props={'style': 'font-weight: bold;'})
        result = node.to_html()
        self.assertEqual(result, '<p>Hello, world!</p>')
        self.assertEqual(node2.to_html(), '<a href="https://example.com">Click here</a>')
        self.assertEqual(node3.to_html(), 'Just some text without a tag')
        self.assertEqual(node4.to_html(), '<b style="font-weight: bold;">Bold text</b>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

if __name__ == '__main__':
    unittest.main()