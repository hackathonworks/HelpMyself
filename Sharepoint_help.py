from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
import os
import pandas as pd

# Replace with your SharePoint site URL and folder path
sharepoint_site_url = "https://yourcompany.sharepoint.com/sites/YourSiteName"
sharepoint_folder_path = "/Shared Documents/FolderName"

# Replace with your email and password
username = "your.email@yourcompany.com"
password = "your_password"

def connect_to_sharepoint(site_url, username, password):
    """Authenticate and connect to SharePoint."""
    ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
    return ctx

def fetch_files_from_folder(ctx, folder_path):
    """
    Fetch files and folders from the given SharePoint folder path.
    Returns a list of tuples (Level 1, Level 2, ..., Filename).
    """
    def traverse_folder(folder, levels):
        """Recursive function to traverse the folder and capture its structure."""
        ctx.load(folder.folders)
        ctx.load(folder.files)
        ctx.execute_query()

        # Add subfolders and their files
        for sub_folder in folder.folders:
            traverse_folder(sub_folder, levels + [sub_folder.name])

        # Add files
        for file in folder.files:
            structure.append(levels + [file.name])

    root_folder = ctx.web.get_folder_by_server_relative_url(folder_path)
    ctx.load(root_folder)
    ctx.execute_query()

    structure = []
    traverse_folder(root_folder, [])
    return structure

def save_to_excel(data, output_file):
    """Save the hierarchical structure to an Excel file."""
    # Find the maximum depth of the hierarchy
    max_depth = max(len(row) for row in data)
    
    # Create a DataFrame with dynamic column names for levels
    columns = [f"Level {i+1}" for i in range(max_depth)]
    df = pd.DataFrame(data, columns=columns)

    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Excel file saved to: {output_file}")

if __name__ == "__main__":
    # Step 1: Connect to SharePoint
    ctx = connect_to_sharepoint(sharepoint_site_url, username, password)

    # Step 2: Fetch folder structure
    print("Fetching folder structure from SharePoint...")
    folder_structure = fetch_files_from_folder(ctx, sharepoint_folder_path)
    print(f"Folder structure fetched. Total items: {len(folder_structure)}")

    # Step 3: Save to Excel
    output_excel_path = "sharepoint_folder_structure.xlsx"
    save_to_excel(folder_structure, output_excel_path)
