import unittest
from blocks import BlockType, block_to_block_type


class TestBlocks(unittest.TestCase):
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
