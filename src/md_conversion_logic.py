from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from enum import Enum
import re


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_node_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        segments = re.split(r"(!\[([^\[\]]*)\]\(([^\(\)]*)\))", old_node.text)
        for index, segment in enumerate(segments):
            if index % 4 == 0:
                if segment:
                    new_nodes.append(TextNode(segment, TextType.NORMAL))
            elif index % 4 == 1:
                result = extract_markdown_images(segment)
                new_nodes.append(TextNode(result[0][0], TextType.IMAGE, result[0][1]))
    return new_nodes


def split_node_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        segments = re.split(r"((?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\))", old_node.text)
        for index, segment in enumerate(segments):
            if index % 4 == 0:
                if segment:
                    new_nodes.append(TextNode(segment, TextType.NORMAL))
            elif index % 4 == 1:
                result = extract_markdown_links(segment)
                new_nodes.append(TextNode(result[0][0], TextType.LINK, result[0][1]))
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        segments = old_node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise Exception
        for index in range(len(segments)):
            if segments[index] == "":
                continue
            elif index % 2 == 0:
                new_nodes.append(TextNode(segments[index], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(segments[index], text_type))

    return new_nodes


def text_to_text_nodes(text):
    old_node = [TextNode(text, TextType.NORMAL)]
    split_by_bold = split_nodes_delimiter(old_node, "**", TextType.BOLD)
    split_by_italic = split_nodes_delimiter(split_by_bold, "_", TextType.ITALIC)
    split_by_code = split_nodes_delimiter(split_by_italic, "`", TextType.CODE)
    split_by_image = split_node_images(split_by_code)
    return split_node_links(split_by_image)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    strip_blocks = list(map(lambda x: x.strip(), raw_blocks))
    blocks = list(filter(lambda x: x != "", strip_blocks))
    return blocks


def block_to_block_type(block):
    check_heading = re.findall(r"^#{1,6} ", block)
    if check_heading:
        return BlockType.HEADING
    check_code = re.findall(r"^```[\s\S]*```$", block)
    if check_code:
        return BlockType.CODE
    split_by_newline = block.split("\n")
    check_quote = list(map(lambda x: re.findall(r"^> ?", x), split_by_newline))
    if [] not in check_quote:
        return BlockType.QUOTE
    check_unordered_list = list(map(lambda x: re.findall(r"^- ", x), split_by_newline))
    if [] not in check_unordered_list:
        return BlockType.UNORDERED_LIST
    check_ordered_list = list(
        map(lambda x: re.findall(r"^\d+\. ", x), split_by_newline)
    )
    truth = True
    if [] in check_ordered_list:
        truth = False
    elif int(check_ordered_list[0][0][0]) != 1:
        truth = False
    else:
        for index in range(len(check_ordered_list)):
            if index > 0:
                if (
                    int(check_ordered_list[index][0][0])
                    - int(check_ordered_list[index - 1][0][0])
                    != 1
                ):
                    truth = False
                    break
    if truth:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_html_node(text):
    text_nodes = text_to_text_nodes(text)
    html_nodes = list(map(lambda x: text_node_to_html_node(x), text_nodes))
    return html_nodes


def markdown_to_html_nodes(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children_of_paragraph = text_to_html_node(block.replace("\n", " "))
                paragraph_node = ParentNode("p", children_of_paragraph)
                children.append(paragraph_node)
            case BlockType.HEADING:
                hash_count = len(re.findall(r"^(#{1,6})", block)[0])
                text = re.findall(r"^#{1,6} (.*)", block)[0].replace("\n", "").strip()
                children_of_heading = text_to_html_node(text)
                heading_node = ParentNode(f"h{hash_count}", children_of_heading)
                children.append(heading_node)
            case BlockType.CODE:
                code_content = re.findall(r"^```([\s\S]*)```$", block)[0]
                child_of_pre = [
                    text_node_to_html_node(TextNode(code_content, TextType.CODE))
                ]
                code_node = ParentNode("pre", child_of_pre)
                children.append(code_node)
            case BlockType.QUOTE:
                split_by_newline = block.split("\n")
                text = " ".join(
                    list(map(lambda x: x.replace(">", "").strip(), split_by_newline))
                )
                children_of_quote = text_to_html_node(text)
                quote_node = ParentNode("blockquote", children_of_quote)
                children.append(quote_node)
            case BlockType.UNORDERED_LIST:
                split_by_newline = block.split("\n")
                children_of_unordered_list = []
                for newline in split_by_newline:
                    children_of_newline = text_to_html_node(
                        newline.replace("-", "").strip()
                    )
                    children_of_unordered_list.append(
                        ParentNode("li", children_of_newline)
                    )
                unordered_list_node = ParentNode("ul", children_of_unordered_list)
                children.append(unordered_list_node)
            case BlockType.ORDERED_LIST:
                split_by_newline = block.split("\n")
                clean_split_by_newline = list(
                    map(
                        lambda x: re.findall(r"^\d+\. (.*)", x)[0].strip(),
                        split_by_newline,
                    )
                )
                children_of_ordered_list = []
                for newline in clean_split_by_newline:
                    children_of_newline = text_to_html_node(newline)
                    children_of_ordered_list.append(
                        ParentNode("li", children_of_newline)
                    )
                ordered_list_node = ParentNode("ol", children_of_ordered_list)
                children.append(ordered_list_node)
    return ParentNode("div", children)
