class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: HTMLNode = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def props_to_html(self):
        text = ' '
        if self.props is None:
            return ''
        result = self.props.items()
        for key, value in result:
            attr = f'{key}="{value}"'
            text += attr + ' '
        return text.rstrip()
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value
        if self.props is None:
            result = f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            props_str = self.props_to_html()
            result = f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
        return result
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], prop: dict = None):
        super().__init__(tag, None, children, prop)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("ParentNode must have children.")
        
        children_html = ''

        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise TypeError("Children must be instances of HTMLNode.")
            children_html += child.to_html()

        if self.props is None:
            return f'<{self.tag}>{children_html}</{self.tag}>'
        
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'