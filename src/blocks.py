from enum import Enum
from htmlnode import *
from split_nodes import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    for line in markdown.split('\n\n'):
        stripped_line = line.strip()
        if stripped_line == '':
            continue
        result.append(stripped_line)
    return result

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'

def block_to_block_type(md_string: str) -> BlockType:
    if md_string.startswith('# ') or md_string.startswith('## ') or md_string.startswith('### ') or md_string.startswith('#### ') or md_string.startswith('##### ') or md_string.startswith('###### '):
        return BlockType.HEADING
    
    elif md_string.startswith("```\n") and md_string.endswith("```"):
        return BlockType.CODE
    
    elif md_string.startswith(">") or md_string.startswith("> "):
        for line in md_string.split('\n'):
            if not (line.startswith('>') or line.startswith('> ')):
                raise ValueError('Quotes must start with ">"')
        return BlockType.QUOTE
    
    elif md_string.startswith("- "):
        for line in md_string.split('\n'):
            if not line.startswith('- '):
                raise ValueError('Unordered lists\' bullet points must all start with "- "')
        return BlockType.UNORDERED_LIST
            
    elif md_string[0].isnumeric() and md_string[1] == ".":
        line_counter = 1
        for line in md_string.split('\n'):
            parts = line.split(".", 1)
            bulletpoint_number = int(parts[0])
            if not (line[0].isnumeric() and parts[1].startswith(" ")):
                raise ValueError('Ordered lists must start with a number followed by a "."')
            elif bulletpoint_number < 1:
                raise ValueError('Ordered lists numbering can\'t start with zero or neagtive numbers')
            elif bulletpoint_number != line_counter:
                raise ValueError('The order of the bullet points must be constantly incrementing')
            line_counter += 1
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    result = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        result.append(text_node_to_html_node(textnode))
    return result

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks_list= markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks_list:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(ParentNode('p', text_to_children(block.replace('\n',' '))))
            case BlockType.HEADING:
                new_block = block.split(' ', 1)
                heading_level = len(new_block[0])
                html_nodes.append(ParentNode(f'h{heading_level}', text_to_children(new_block[1])))
            case BlockType.CODE:
                new_block = block.split('```')
                new_node = TextNode(new_block[1].lstrip('\n'), TextType.TEXT)
                code_node = ParentNode('code', [text_node_to_html_node(new_node)])
                html_nodes.append(ParentNode('pre', [code_node]))
            case BlockType.QUOTE:
                lines = []
                for line in block.split('\n'):
                    cleaned = line.lstrip('>').lstrip()
                    lines.append(cleaned)
                new_block = '\n'.join(lines)
                html_nodes.append(ParentNode('blockquote', text_to_children(new_block)))
            case BlockType.UNORDERED_LIST:
                list_items = []
                for line in block.split('\n'):
                    text = line[2:].strip()
                    list_items.append(ParentNode('li', text_to_children(text)))
                html_nodes.append(ParentNode('ul', list_items))
            case BlockType.ORDERED_LIST:
                list_items = []
                for item in block.split('\n'):
                    text = item.split('. ',1)
                    list_items.append(ParentNode('li', text_to_children(text[1])))
                html_nodes.append(ParentNode('ol', list_items))
    return ParentNode('div', html_nodes)
        
