import unittest

from textnode import TextNode, TextType


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

    def test_text_to_html_node(self):
        node = TextNode("hello", TextType.NORMAL)
        result = node.text_to_html_node()
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "hello")
        node1 = TextNode("hello", TextType.BOLD)
        result1 = node1.text_to_html_node()
        self.assertEqual(result1.tag, "b")
        self.assertEqual(result1.value, "hello")
        node2 = TextNode("hello", TextType.ITALIC)
        result2 = node2.text_to_html_node()
        self.assertEqual(result2.tag, "i")
        self.assertEqual(result2.value, "hello")
        node3 = TextNode("code_snippet", TextType.CODE)
        result3 = node3.text_to_html_node()
        self.assertEqual(result3.tag, "code")
        self.assertEqual(result3.value, "code_snippet")
        node4 = TextNode("anchor text", TextType.LINK, "www.google.com")
        result4 = node4.text_to_html_node()
        self.assertEqual(result4.tag, "a")
        self.assertEqual(result4.value, "anchor text")
        self.assertEqual(result4.props, {"href": "www.google.com"})
        node5 = TextNode("alt text", TextType.IMAGE, "sunset.jpg")
        result5 = node5.text_to_html_node()
        self.assertEqual(result5.tag, "img")
        self.assertEqual(result5.value, "")
        self.assertEqual(result5.props, {"src": "sunset.jpg", "alt": "alt text"})


if __name__ == "__main__":
    unittest.main()
