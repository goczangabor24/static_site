import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    result = re.findall(r'!\[(.*?)\].*?(http.*?)\)', text)
    return result

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    result = re.findall(r'(?<!\!)\[(.*?)\].*?(http.*?)\)', text)
    return result