import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_default_tag(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
        node1 = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com"')
        node2 = HTMLNode(props={"target": "_blank"})
        self.assertEqual(node2.props_to_html(), ' target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        node1 = LeafNode(None, "hello")
        self.assertEqual("hello", node1.to_html())
        node3 = LeafNode("p", "hello", {"href": "https://www.google.com"})
        self.assertEqual('<p href="https://www.google.com">hello</p>', node3.to_html())


if __name__ == "__main__":
    unittest.main()
