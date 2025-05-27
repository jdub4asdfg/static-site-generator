import unittest
from textnode import TextNode, TextType
from standalone import (
    text_to_html_node,
    text_to_text_nodes,
    split_nodes_delimiter,
    split_node_images,
    split_node_links,
    extract_markdown_links,
    extract_markdown_images,
)


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
        old_nodes = [
            TextNode("`code block` hello", TextType.NORMAL),
            TextNode("`another code block``console.log`", TextType.NORMAL),
        ]
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(result[0].text, "code block")
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, " hello")
        self.assertEqual(result[1].text_type, TextType.NORMAL)
        self.assertEqual(result[2].text, "another code block")
        self.assertEqual(result[2].text_type, TextType.CODE)
        self.assertEqual(result[3].text, "console.log")
        self.assertEqual(result[3].text_type, TextType.CODE)
        old_nodes2 = [
            TextNode("**bold text** hello", TextType.NORMAL),
            TextNode("**another bold text****good morning**", TextType.NORMAL),
        ]
        result = split_nodes_delimiter(old_nodes2, "**", TextType.BOLD)
        self.assertEqual(result[0].text, "bold text")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " hello")
        self.assertEqual(result[1].text_type, TextType.NORMAL)
        self.assertEqual(result[2].text, "another bold text")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "good morning")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        old_nodes3 = [TextNode("_unclosed italics", TextType.NORMAL)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes3, "_", TextType.ITALIC)

    def test_extract_markdown_images(self):
        text = "This is an image ![image](https://image.com/image), this is also an image ![image again](https://imageagain.com/wowzers)."
        result = extract_markdown_images(text)
        self.assertEqual(
            [
                ("image", "https://image.com/image"),
                ("image again", "https://imageagain.com/wowzers"),
            ],
            result,
        )
        text2 = "[decoy] and real image here ![image](https://image.com/image)."
        result2 = extract_markdown_images(text2)
        self.assertEqual([("image", "https://image.com/image")], result2)

    def test_extract_markdown_links(self):
        text = "This is a link to [instagram](https://www.instagram.com) and this is a link to [the facebook](https://www.facebook.com)."
        result = extract_markdown_links(text)
        self.assertEqual(
            [
                ("instagram", "https://www.instagram.com"),
                ("the facebook", "https://www.facebook.com"),
            ],
            result,
        )
        text2 = "(decoy) and real link here [link](https://www.link.com)."
        result2 = extract_markdown_links(text2)
        self.assertEqual([("link", "https://www.link.com")], result2)

    def test_split_node_links(self):
        old_nodes = [
            TextNode("This is a link [link](https://www.google.com).", TextType.NORMAL),
            TextNode(
                "[another link](https://www.instagram.com) and [yet another link](https://www.facebook.com)",
                TextType.NORMAL,
            ),
        ]
        result = split_node_links(old_nodes)
        self.assertEqual(result[0].text, "This is a link ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://www.google.com")
        self.assertEqual(result[2].text, ".")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        self.assertEqual(result[3].text, "another link")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].url, "https://www.instagram.com")
        self.assertEqual(result[4].text, " and ")
        self.assertEqual(result[4].text_type, TextType.NORMAL)
        self.assertEqual(result[5].text, "yet another link")
        self.assertEqual(result[5].text_type, TextType.LINK)
        self.assertEqual(result[5].url, "https://www.facebook.com")

    def test_split_node_images(self):
        old_nodes = [
            TextNode("This is an image ![image](image.jpg).", TextType.NORMAL),
            TextNode(
                "![another image](picture.png) and ![yet another image](picture.jpg)",
                TextType.NORMAL,
            ),
        ]
        result = split_node_images(old_nodes)
        self.assertEqual(result[0].text, "This is an image ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "image.jpg")
        self.assertEqual(result[2].text, ".")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        self.assertEqual(result[3].text, "another image")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "picture.png")
        self.assertEqual(result[4].text, " and ")
        self.assertEqual(result[4].text_type, TextType.NORMAL)
        self.assertEqual(result[5].text, "yet another image")
        self.assertEqual(result[5].text_type, TextType.IMAGE)
        self.assertEqual(result[5].url, "picture.jpg")

    def test_text_to_text_nodes(self):
        text = "Hello, this is **bold**, _italic_ and `code`. This is an image ![image](tungsahur.jpg) and this is a link [link](https://www.facebook.com)"
        result = text_to_text_nodes(text)
        self.assertEqual(result[0].text, "Hello, this is ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, ", ")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " and ")
        self.assertEqual(result[4].text_type, TextType.NORMAL)
        self.assertEqual(result[5].text, "code")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, ". This is an image ")
        self.assertEqual(result[6].text_type, TextType.NORMAL)
        self.assertEqual(result[7].text, "image")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].url, "tungsahur.jpg")
        self.assertEqual(result[8].text, " and this is a link ")
        self.assertEqual(result[8].text_type, TextType.NORMAL)
        self.assertEqual(result[9].text, "link")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].url, "https://www.facebook.com")
        text2 = "Hello, this should raise an **error"
        with self.assertRaises(Exception):
            text_to_text_nodes(text2)


if __name__ == "__main__":
    unittest.main()
