from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


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
