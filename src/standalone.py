from textnode import TextNode, TextType
from htmlnode import LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == text_type:
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


def text_to_html_node(text_node):
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
