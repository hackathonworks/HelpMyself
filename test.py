!pip install anytree
import os
import zipfile
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

def extract_zip(zip_path, extract_to):
    """Extracts a zip file to a specified directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted all files to: {extract_to}")

def generate_file_tree(extract_to):
    """Generates a tree structure using anytree from the extracted files."""
    root_nodes = {}
    file_tree_root = Node("root")  # Root of the tree

    for root, dirs, files in os.walk(extract_to):
        # Add directories to the tree
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            relative_path = os.path.relpath(dir_path, extract_to)
            parent_path = os.path.dirname(relative_path)
            parent_node = root_nodes.get(parent_path, file_tree_root)
            dir_node = Node(dir_name, parent=parent_node)
            root_nodes[relative_path] = dir_node

        # Add files to the tree
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, extract_to)
            parent_path = os.path.dirname(relative_path)
            parent_node = root_nodes.get(parent_path, file_tree_root)
            Node(file_name, parent=parent_node)

    return file_tree_root

def visualize_tree(root_node, output_dot_file="file_tree.dot", output_image="file_tree.png"):
    """Visualizes the tree using anytree and saves it as a DOT file and image."""
    for pre, fill, node in RenderTree(root_node):
        print(f"{pre}{node.name}")

    # Export the tree structure to a DOT file
    DotExporter(root_node).to_dotfile(output_dot_file)
    print(f"Tree structure saved as DOT file: {output_dot_file}")

    # Optional: Convert DOT file to an image (requires Graphviz installed)
    try:
        from subprocess import run
        run(["dot", "-Tpng", output_dot_file, "-o", output_image], check=True)
        print(f"Tree structure saved as image: {output_image}")
    except Exception as e:
        print("Graphviz not found or failed to generate image. Install Graphviz to enable image generation.")

# Example usage
if __name__ == "__main__":
    zip_file_path = "sample.zip"  # Path to the zip file
    extract_directory = "extracted_files"  # Destination folder for extraction
    output_dot_path = "file_tree.dot"  # Output DOT file path
    output_image_path = "file_tree.png"  # Output image file path

    # Extract and generate the tree
    extract_zip(zip_file_path, extract_directory)
    root = generate_file_tree(extract_directory)
    visualize_tree(root, output_dot_path, output_image_path)
