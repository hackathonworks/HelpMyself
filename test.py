import os
import zipfile
import pandas as pd

def extract_and_list_with_levels(zip_path, extract_to, output_excel):
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted all files to {extract_to}")
    
    # Create a list to store level-wise file structure
    file_structure = []

    for root, dirs, files in os.walk(extract_to):
        for name in dirs + files:
            relative_path = os.path.relpath(os.path.join(root, name), extract_to)
            parts = relative_path.split(os.sep)
            file_structure.append(parts)
    
    # Determine the maximum depth (number of levels)
    max_depth = max(len(parts) for parts in file_structure)
    
    # Normalize the structure so all rows have the same number of levels
    normalized_structure = [
        parts + [''] * (max_depth - len(parts)) for parts in file_structure
    ]
    
    # Convert to DataFrame with levels as columns
    columns = [f"Level {i+1}" for i in range(max_depth)]
    df = pd.DataFrame(normalized_structure, columns=columns)
    
    # Save to Excel
    df.to_excel(output_excel, index=False)
    print(f"File structure with levels saved to {output_excel}")

# Example usage
zip_file_path = "/content/sample.zip"  # Replace with your zip file path
extract_directory = "extracted_files"  # Replace with your desired extraction folder
output_excel_path = "file_structure_with_levels.xlsx"  # Replace with your desired Excel file path

extract_and_list_with_levels(zip_file_path, extract_directory, output_excel_path)
