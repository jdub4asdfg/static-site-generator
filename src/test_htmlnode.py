import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(None, [LeafNode(None, "hello")])
        with self.assertRaises(ValueError):
            node.to_html()
        node1 = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node1.to_html()
        node2 = ParentNode("p", [LeafNode("p", "hello")])
        self.assertEqual("<p><p>hello</p></p>", node2.to_html())
        node3 = ParentNode(
            "p",
            [
                LeafNode("b", "hello"),
                LeafNode(None, "hi"),
                LeafNode("i", "nihao"),
                LeafNode(None, "bonjour"),
            ],
        )
        self.assertEqual("<p><b>hello</b>hi<i>nihao</i>bonjour</p>", node3.to_html())
        node4 = ParentNode("p", [LeafNode("p", "hello")], {"href": "www.wow.com"})
        self.assertEqual('<p href="www.wow.com"><p>hello</p></p>', node4.to_html())
        node5 = ParentNode(
            "p",
            [
                LeafNode("b", "hello"),
                LeafNode(None, "hi"),
                LeafNode("i", "nihao"),
                LeafNode(None, "bonjour"),
            ],
            {"href": "www.wow.com", "target": "_blank"},
        )
        self.assertEqual(
            '<p href="www.wow.com" target="_blank"><b>hello</b>hi<i>nihao</i>bonjour</p>',
            node5.to_html(),
        )
        node6 = ParentNode("p", [ParentNode("div", [LeafNode("i", "hello")])])
        self.assertEqual("<p><div><i>hello</i></div></p>", node6.to_html())
        node7 = ParentNode(
            "p",
            [
                ParentNode("div", [LeafNode("i", "hello")]),
                ParentNode("b", [LeafNode(None, "hi")]),
            ],
        )
        self.assertEqual("<p><div><i>hello</i></div><b>hi</b></p>", node7.to_html())


if __name__ == "__main__":
    unittest.main()
