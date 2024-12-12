import pandas as pd
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

def read_excel(file_path):
    """Reads an Excel file containing levels and returns it as a DataFrame."""
    df = pd.read_excel(file_path)
    return df

def build_tree_from_levels(df):
    """
    Builds a hierarchical tree using anytree based on level columns.
    Assumes that columns are named 'Level 1', 'Level 2', ..., 'Level N'.
    """
    # Create a root node
    root = Node("root")

    # Dictionary to store parent nodes for each level
    level_nodes = {0: root}

    # Iterate over each row to build the tree
    for _, row in df.iterrows():
        parent = root
        for level in range(len(row)):
            level_name = row[f"Level {level+1}"]
            if pd.isna(level_name) or level_name == '':
                break  # Stop if we reach empty cells
            
            # Create or retrieve the node
            existing_node = next((node for node in parent.children if node.name == level_name), None)
            if not existing_node:
                new_node = Node(level_name, parent=parent)
                parent = new_node
                level_nodes[level + 1] = new_node
            else:
                parent = existing_node  # Move to the existing node for the next level

    return root

def visualize_tree(root_node, output_dot_file="tree_from_excel.dot", output_image="tree_from_excel.png"):
    """
    Visualizes the tree and saves it as a DOT file and an optional PNG image.
    """
    # Print tree to terminal
    for pre, fill, node in RenderTree(root_node):
        print(f"{pre}{node.name}")

    # Export to DOT file
    DotExporter(root_node).to_dotfile(output_dot_file)
    print(f"Tree structure saved as DOT file: {output_dot_file}")

    # Generate image (requires Graphviz installed)
    try:
        from subprocess import run
        run(["dot", "-Tpng", output_dot_file, "-o", output_image], check=True)
        print(f"Tree structure saved as image: {output_image}")
    except Exception as e:
        print("Graphviz not found or failed to generate image. Install Graphviz to enable image generation.")

# Example usage
if __name__ == "__main__":
    excel_file_path = "file_structure_with_levels.xlsx"  # Path to the Excel file
    output_dot_path = "tree_from_excel.dot"  # Output DOT file path
    output_image_path = "tree_from_excel.png"  # Output image file path

    # Read the Excel file and build the tree
    df = read_excel(excel_file_path)
    tree_root = build_tree_from_levels(df)

    # Visualize the tree
    visualize_tree(tree_root, output_dot_path, output_image_path)
