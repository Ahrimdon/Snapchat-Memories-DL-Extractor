import os
import zipfile
from tqdm import tqdm

def extract_files(zip_files_directory, extract_to_directory):
    # Ensure the extract_to_directory exists
    os.makedirs(extract_to_directory, exist_ok=True)

    # Iterate over all files in the directory containing the zip files
    for file_name in os.listdir(zip_files_directory):
        # Check if the file is a zip file
        if file_name.endswith('.zip'):
            # Construct full file path
            file_path = os.path.join(zip_files_directory, file_name)
            # Open the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # List of members to extract
                members = [member for member in zip_ref.namelist() if member.startswith('memories/')]
                # Total number of items to extract (for progress bar)
                total_members = len(members)
                # Extract only the 'memories' folder
                with tqdm(total=total_members, desc=f"Extracting {file_name}", unit='files') as pbar:
                    for member in members:
                        zip_ref.extract(member, extract_to_directory)
                        pbar.update(1)  # Update the progress bar by one each time a file is extracted

    print(f"All 'memories' folders have been extracted to {extract_to_directory}")

def main():
    zip_files_directory = 'C:\\path\\to\\zipfiles\\folder\\'
    extract_to_directory = 'C:\\path\\to\\extraction\\folder\\'
    extract_files(zip_files_directory, extract_to_directory)

if __name__ == '__main__':
    main()