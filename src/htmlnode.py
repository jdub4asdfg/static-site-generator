import functools


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Child classes will override this method
        raise NotImplementedError

    def props_to_html(self):
        attributes = functools.reduce(
            lambda x, y: x + f' {y[0]}="{y[1]}"', self.props.items(), ""
        )
        return attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        elif self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        elif self.children is None:
            raise ValueError
        else:
            string_of_children = functools.reduce(
                lambda x, y: x + y.to_html(), self.children, ""
            )
            if self.props is None:
                return_string = f"<{self.tag}>{string_of_children}</{self.tag}>"
            else:
                return_string = f"<{self.tag}{self.props_to_html()}>{string_of_children}</{self.tag}>"

        return return_string
