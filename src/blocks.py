from enum import Enum

def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    for line in markdown.split('\n\n'):
        stripped_line = line.strip()
        if stripped_line == '':
            continue
        result.append(stripped_line)
    return result

class BlockType(Enum):
    paragraph = 'paragraph'
    heading = 'heading'
    code = 'code'
    quote = 'quote'
    unordered_list = 'unordered list'
    ordered_list = 'ordered list'

def block_to_block_type(md_string: str) -> BlockType:
    if md_string.startswith('# ') or md_string.startswith('## ') or md_string.startswith('### ') or md_string.startswith('#### ') or md_string.startswith('##### ') or md_string.startswith('###### '):
        return BlockType.heading
    
    elif md_string.startswith("```\n") and md_string.endswith("```"):
        return BlockType.code
    
    elif md_string.startswith(">") or md_string.startswith("> "):
        for line in md_string.split('\n'):
            if not (line.startswith('>') or line.startswith('> ')):
                raise ValueError('Quotes must start with ">"')
        return BlockType.quote
    
    elif md_string.startswith("- "):
        for line in md_string.split('\n'):
            if not line.startswith('- '):
                raise ValueError('Unordered lists\' bullet points must all start with "- "')
        return BlockType.unordered_list
            
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
        return BlockType.ordered_list
    
    else:
        return BlockType.paragraph