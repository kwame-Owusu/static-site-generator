from textnode import TextType, TextNode 
from block_markdown import markdown_to_html_node
import os
import shutil
import sys
 
if len(sys.argv) > 1:
    base_path = sys.argv[1]
else:
    base_path= '/'

def move_static_to_public(source_dir, destination_dir) -> None:
    # Clear the destination directory first
    public_path = 'docs/'
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
    for line in markdown.splitlines():  # Split the markdown content into lines
        if line.startswith('#'):  # Look for the first header
            return line.strip("#").strip()  
    raise Exception("No header found in markdown input")


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    markdown_content = ""
    template_content = ""

    #read markdown content
    with open(from_path, 'r') as markdown_file:
        lines = markdown_file.read()
        markdown_content += lines
        markdown_res = markdown_to_html_node(markdown_content).to_html()

    #read template content  
    with open(template_path, "r") as template_file:
        lines = template_file.read()
        template_content += lines

        # Extract title and replace placeholders
        template_title = extract_title(markdown_content)
        template_content = template_content.replace('{{ Title }}', template_title)
        template_content = template_content.replace('{{ Content }}', markdown_res)

        template_content = template_content.replace('href="/', f'href="{base_path}')
        template_content = template_content.replace('src="/', f'src="{base_path}')
      # Ensure directories exist before writing the file
    if os.path.dirname(dest_path):  # Check parent directory
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final content to the destination path
    with open(dest_path, "w") as file:
        file.write(template_content) 

def generate_pages_recursively(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str) -> None:
    for root, dirs, files in os.walk(dir_path_content):
        for file_item in files:
            if file_item.endswith(".md"):
                # Build the full path to the markdown file
                file_path = os.path.join(root, file_item)

                # Calculate the relative path, and construct the destination path
                rel_path = os.path.relpath(root, dir_path_content)
                dest_dir = os.path.join("docs", rel_path)

                # Ensure the directory exists
                os.makedirs(dest_dir, exist_ok=True)

                # Create the destination html file path
                dest_file_name = os.path.splitext(file_item)[0] + ".html"
                dest_dir_path = os.path.join(dest_dir, dest_file_name)

                # Generate the HTML file
                generate_page(file_path, template_path, dest_dir_path, base_path)



def main() -> None:
    source_directory = "static/"
    destination_directory = "docs/"
    template_path = "template.html"
    
    #Move static files to public directory
    move_static_to_public(source_directory, destination_directory)
    
    generate_pages_recursively("content/", template_path, destination_directory, base_path)


   
    print("Page generation complete. Visit: http://localhost:8888")

if __name__ == "__main__":
    main()