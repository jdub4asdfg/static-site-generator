import unittest
from textnode import TextNode, TextType
from functions import (
    text_node_to_html_node,
    text_to_text_nodes,
    split_nodes_delimiter,
    split_node_images,
    split_node_links,
    extract_markdown_links,
    extract_markdown_images,
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_nodes,
)


class TestFunctions(unittest.TestCase):
    def test_text_to_html_node(self):
        node = TextNode("hello", TextType.NORMAL)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "hello")
        node1 = TextNode("hello", TextType.BOLD)
        result1 = text_node_to_html_node(node1)
        self.assertEqual(result1.tag, "b")
        self.assertEqual(result1.value, "hello")
        node2 = TextNode("hello", TextType.ITALIC)
        result2 = text_node_to_html_node(node2)
        self.assertEqual(result2.tag, "i")
        self.assertEqual(result2.value, "hello")
        node3 = TextNode("code_snippet", TextType.CODE)
        result3 = text_node_to_html_node(node3)
        self.assertEqual(result3.tag, "code")
        self.assertEqual(result3.value, "code_snippet")
        node4 = TextNode("anchor text", TextType.LINK, "www.google.com")
        result4 = text_node_to_html_node(node4)
        self.assertEqual(result4.tag, "a")
        self.assertEqual(result4.value, "anchor text")
        self.assertEqual(result4.props, {"href": "www.google.com"})
        node5 = TextNode("alt text", TextType.IMAGE, "sunset.jpg")
        result5 = text_node_to_html_node(node5)
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

    def test_block_to_block_type(self):
        block = "### Heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
        block2 = "####### Heading"
        result2 = block_to_block_type(block2)
        self.assertEqual(result2, BlockType.PARAGRAPH)
        block3 = "```print('hello world')```"
        result3 = block_to_block_type(block3)
        self.assertEqual(result3, BlockType.CODE)
        block4 = """```print('hello')
markdown = '```hello = 1```'
print(hello)```"""
        result4 = block_to_block_type(block4)
        self.assertEqual(result4, BlockType.CODE)
        block5 = "```unclosed"
        result5 = block_to_block_type(block5)
        self.assertEqual(result5, BlockType.PARAGRAPH)
        block6 = """>This is a quote
> This is also a quote
This is not a quote"""
        result6 = block_to_block_type(block6)
        self.assertEqual(result6, BlockType.PARAGRAPH)
        block7 = """> This is a quote
>This is also a quote"""
        result7 = block_to_block_type(block7)
        self.assertEqual(result7, BlockType.QUOTE)
        block8 = """- This is line 1
-This is where it ends"""
        result8 = block_to_block_type(block8)
        self.assertEqual(result8, BlockType.PARAGRAPH)
        block9 = """- This is line 1
- There must be a space"""
        result9 = block_to_block_type(block9)
        self.assertEqual(result9, BlockType.UNORDERED_LIST)
        block10 = """1. Line 1
2.123"""
        result10 = block_to_block_type(block10)
        self.assertEqual(result10, BlockType.PARAGRAPH)
        block11 = """1. Line 1
2. Line 2
3. Line 3"""
        result11 = block_to_block_type(block11)
        self.assertEqual(result11, BlockType.ORDERED_LIST)
        block12 = """1. Line 1
2. Line 2
4. Line 3"""
        result12 = block_to_block_type(block12)
        self.assertEqual(result12, BlockType.PARAGRAPH)

    def test_markdown_to_blocks(self):
        markdown = """
First block

Second block
Another line on second block


 Third block
Second line on third block 
        """
        result = markdown_to_blocks(markdown)
        self.assertEqual(
            result,
            [
                "First block",
                "Second block\nAnother line on second block",
                "Third block\nSecond line on third block",
            ],
        )
        markdown2 = """
 First block 


Second block
Another line on second block 

Third block 
        """
        result2 = markdown_to_blocks(markdown2)
        self.assertEqual(
            result2,
            [
                "First block",
                "Second block\nAnother line on second block",
                "Third block",
            ],
        )

    def test_markdown_to_html_nodes(self):
        markdown = """This is the **first** line.
This is the _second_ line.
This is the third line."""
        result = markdown_to_html_nodes(markdown).to_html()
        self.assertEqual(
            result,
            "<div><p>This is the <b>first</b> line. This is the <i>second</i> line. This is the third line.</p></div>",
        )
        markdown1 = """```print('hello world')
print('bruh')```

>Do or do not, there is no **try**.
>If you were the inventors of _Facebook_, you would've invented **Facebook**."""
        result1 = markdown_to_html_nodes(markdown1).to_html()
        self.assertEqual(
            result1,
            "<div><pre><code>print('hello world')\nprint('bruh')</code></pre><blockquote>Do or do not, there is no <b>try</b>. If you were the inventors of <i>Facebook</i>, you would've invented <b>Facebook</b>.</blockquote></div>",
        )
        markdown2 = "#### Heading"
        result2 = markdown_to_html_nodes(markdown2).to_html()
        self.assertEqual(result2, "<div><h4>Heading</h4></div>")
        markdown3 = "####### Paragraph"
        result3 = markdown_to_html_nodes(markdown3).to_html()
        self.assertEqual(result3, "<div><p>####### Paragraph</p></div>")
        markdown4 = """- Item 1
- Item 2
- Item 3

1. Item 1
2. Item 2
3. Item 3"""
        result4 = markdown_to_html_nodes(markdown4).to_html()
        self.assertEqual(
            result4,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
