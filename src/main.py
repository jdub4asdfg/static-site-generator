from textnode import *
from htmlnode import *

def main():
    test = TextNode('hi', 'link', 'www.wow.com')
    test2_child = HTMLNode()
    test2 = HTMLNode('h1', 'hello', [test2_child], {"href": "https://www.google.com"})
    print(test)
    print(test2)

main()
