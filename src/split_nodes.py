from textnode import TextNode, TextType
from extract_markdown_images import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        elif node.text.count(delimiter) == 0:
            new_nodes.append(node)
            continue
        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Delimiters in '{node.text}' are not balanced.")
        else:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, text_type.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        extracted_tuple = extract_markdown_images(node.text)
        remaining_text = node.text
        if node.text_type != TextType.TEXT or extracted_tuple == []:
            new_nodes.append(node)
            continue
        else:
           for alt_text, url in extracted_tuple:
                new_url = f'![{alt_text}]({url})'
                section = remaining_text.split(new_url, 1)
                if section[0] != '':
                    new_nodes.append(TextNode(section[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                else:
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))    
                remaining_text = section[1]
        if remaining_text != '':
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        extracted_tuple = extract_markdown_links(node.text)
        remaining_text = node.text
        if node.text_type != TextType.TEXT or extracted_tuple == []:
            new_nodes.append(node)
            continue
        else:
            for link_text, url in extracted_tuple:
                new_url = f'[{link_text}]({url})'
                section = remaining_text.split(new_url, 1)
                if section[0] != '':
                    new_nodes.append(TextNode(section[0], TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                else:
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                remaining_text = section[1]
        if remaining_text != '':
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    string_to_node = [TextNode(text, TextType.TEXT)]
    first = split_nodes_delimiter(string_to_node, '**', TextType.BOLD)
    second = split_nodes_delimiter(first, "_", TextType.ITALIC)
    third = split_nodes_delimiter(second, "`", TextType.CODE)
    fourth = split_nodes_image(third)
    result = split_nodes_link(fourth)
    return result