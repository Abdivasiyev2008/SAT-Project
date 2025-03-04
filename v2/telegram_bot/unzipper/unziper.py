import os
import re
from unzipper.file_processor import process_directory
import pyzipper

def extract_and_process(zip_file_path, password=None):
    """
    Extracts the contents of a .zip file using a password if provided,
    and processes any .txt files inside.
    """
    # Define the output folder based on the zip file name (without the .zip extension)
    output_folder = zip_file_path.replace('.zip', '')  

    # Check if output_folder is an existing file; rename it if necessary to avoid conflict
    if os.path.isfile(output_folder):
        output_folder += "_extracted"  # Rename the folder to avoid conflict with file names

    # Create the output folder if it does not already exist
    os.makedirs(output_folder, exist_ok=True)

    # Attempt to extract the zip file
    try:
        # Open and extract the zip file using pyzipper
        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
            if password:
                # Set the password if provided
                zip_file.setpassword(password.encode())
            zip_file.extractall(output_folder)  # Extract contents to output folder
            print(f"Extracted {zip_file_path} to {output_folder}")
            
            # Process any .txt files inside the extracted folder
            process_directory(output_folder)
            
            # Optionally delete the .zip file after successful extraction
            os.remove(zip_file_path)
            print(f"Deleted ZIP file: {zip_file_path}")
            return True

    except Exception as e:
        # Print error message if extraction fails
        print(f"Error extracting file: {e}")
        return False
