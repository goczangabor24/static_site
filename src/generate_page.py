from blocks import markdown_to_blocks

def extract_title(markdown: str) -> str:
    header_count = 0
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()        
    raise Exception("Markdown file must contain a main header")