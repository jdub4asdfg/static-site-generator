import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL, "www.wow.com")
        node2 = TextNode("This is a text node", TextType.NORMAL, "www.wow.com")
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        node3 = TextNode("This might be a text node", TextType.NORMAL)
        self.assertNotEqual(node, node3)
        node4 = TextNode("This might be a text node", TextType.BOLD)
        self.assertNotEqual(node, node4)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertTrue(node.url is None)


if __name__ == "__main__":
    unittest.main()
