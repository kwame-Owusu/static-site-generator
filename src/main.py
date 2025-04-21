from textnode import TextType, TextNode 
import os
import shutil


def move_static_to_public(source_dir, destination_dir) -> None:
    # Clear the destination directory first
    public_path = 'public/'
    if os.path.exists(public_path):
        for item in os.listdir(public_path):
            item_path = os.path.join(public_path, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Copy files and directories from source to destination
    if os.path.exists(source_dir):
        for item in os.listdir(source_dir):
            source_item_path = os.path.join(source_dir, item)
            destination_item_path = os.path.join(destination_dir, item)
            
            if os.path.isfile(source_item_path):
                shutil.copy2(source_item_path, destination_item_path)
            elif os.path.isdir(source_item_path):
                # If the destination directory already exists, remove it first
                if os.path.exists(destination_item_path):
                    shutil.rmtree(destination_item_path)
                shutil.copytree(source_item_path, destination_item_path)

def extract_title(markdown: str) -> str:
    with open(markdown, 'r') as file:
        for line in file:
            if line.startswith('#'):
                return line.strip("#").strip()
        raise Exception("No header found in markdown file")


def main() -> None:
  source_directory = "static/"
  destination_directory = "public/"
  move_static_to_public(source_directory, destination_directory)

if __name__ == "__main__":
    title = extract_title("content/index.md")
    print(title)