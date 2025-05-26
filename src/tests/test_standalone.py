import unittest
from src.textnode import TextNode, TextType
from src.standalone import text_to_html_node, split_nodes_delimiter


class TestStandalone(unittest.TestCase):
    def test_text_to_html_node(self):
        node = TextNode("hello", TextType.NORMAL)
        result = text_to_html_node(node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "hello")
        node1 = TextNode("hello", TextType.BOLD)
        result1 = text_to_html_node(node1)
        self.assertEqual(result1.tag, "b")
        self.assertEqual(result1.value, "hello")
        node2 = TextNode("hello", TextType.ITALIC)
        result2 = text_to_html_node(node2)
        self.assertEqual(result2.tag, "i")
        self.assertEqual(result2.value, "hello")
        node3 = TextNode("code_snippet", TextType.CODE)
        result3 = text_to_html_node(node3)
        self.assertEqual(result3.tag, "code")
        self.assertEqual(result3.value, "code_snippet")
        node4 = TextNode("anchor text", TextType.LINK, "www.google.com")
        result4 = text_to_html_node(node4)
        self.assertEqual(result4.tag, "a")
        self.assertEqual(result4.value, "anchor text")
        self.assertEqual(result4.props, {"href": "www.google.com"})
        node5 = TextNode("alt text", TextType.IMAGE, "sunset.jpg")
        result5 = text_to_html_node(node5)
        self.assertEqual(result5.tag, "img")
        self.assertEqual(result5.value, "")
        self.assertEqual(result5.props, {"src": "sunset.jpg", "alt": "alt text"})

    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode('`code block` hello', TextType.NORMAL), TextNode('`another code block``console.log`', TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, '`', TextType.CODE)
        self.assertEqual(result[0].text, 'code block')
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, ' hello')
        self.assertEqual(result[1].text_type, TextType.NORMAL)
        self.assertEqual(result[2].text, 'another code block')
        self.assertEqual(result[2].text_type, TextType.CODE)
        self.assertEqual(result[3].text, 'console.log')
        self.assertEqual(result[3].text_type, TextType.CODE)
        old_nodes2 = [TextNode('**bold text** hello', TextType.NORMAL), TextNode('**another bold text****good morning**', TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes2, '**', TextType.BOLD)
        self.assertEqual(result[0].text, 'bold text')
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, ' hello')
        self.assertEqual(result[1].text_type, TextType.NORMAL)
        self.assertEqual(result[2].text, 'another bold text')
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, 'good morning')
        self.assertEqual(result[3].text_type, TextType.BOLD)
        old_nodes3 = [TextNode('_unclosed italics', TextType.NORMAL)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes3, '_', TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
