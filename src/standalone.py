from textnode import TextNode, TextType
from htmlnode import LeafNode
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
