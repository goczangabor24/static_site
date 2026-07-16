# from textnode_creator import TextNode, TextType
from copy_static import copy_files_recursive
import os
import shutil

def main():

    dest_dir_path = "./public"
    source_dir_path = "./static"

    # node = TextNode("Hello, World!", TextType.text, None)
    # print(node)
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    copy_files_recursive(source_dir_path, dest_dir_path)

main()