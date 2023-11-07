import requests
import urllib3
from urllib.parse import urlparse, parse_qs, unquote
import os
from tqdm import tqdm
import time
from colorama import init, Fore

# Initialize colorama to add colors to the terminal output
init(autoreset=True)

# Disable warnings that pop up when making unverified HTTP requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_file(url, output_dir):
    """
    Download a file from a given URL to the specified output directory.

    Args:
    - url (str): The URL of the file to be downloaded.
    - output_dir (str): The directory where the file will be saved.

    Returns:
    - filename (str): The path to the saved file.
    """
    
    # Send a GET request to the URL, stream the content (i.e., download in chunks) and ignore SSL verification
    with requests.get(url, stream=True, verify=False) as r:
        # Raise an exception if the request returned an HTTP error
        r.raise_for_status()

        # Determine the filename
        if 'content-disposition' in r.headers:
            content_disposition = r.headers['content-disposition']
            filename = unquote(content_disposition.split('filename=')[-1].strip('";\''))
        else:
            # Parse the URL to get the path and then get the last part of the path as the filename
            url_path = urlparse(url).path
            filename = os.path.basename(url_path)

        # Combine the output directory and filename for the full path
        full_path = os.path.join(output_dir, filename)

        print(f"\nDownloading {url} to {full_path}")

        # Create directories if they don't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get the file size for the progress bar
        total_size_in_bytes = int(r.headers.get('content-length', 0)) if r.headers.get('content-length') else None

        # Set up the progress bar using tqdm and colorama
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, dynamic_ncols=True,
                            bar_format=f"{Fore.GREEN}{{l_bar}}{Fore.BLUE}{{bar}}{Fore.YELLOW}{{n_fmt}}{Fore.WHITE}/{Fore.CYAN}{{total_fmt}} {Fore.RED}[{{elapsed}}<{Fore.GREEN}{{remaining}}, {Fore.WHITE}{{rate_fmt}}{{postfix}}{Fore.RESET}]")

        # Save the file in chunks
        with open(full_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()

    return full_path

def process_file(input_filename, parent_dir, output_dir):
    # Use the full path to the file
    full_path_to_file = os.path.join(parent_dir, input_filename)

    # Read URLs from file
    with open(full_path_to_file, 'r') as f:
        urls = f.read().splitlines()

    # Get sleep time between downloads
    # sleep_time_input = input("Enter the time to sleep between downloads to avoid rate limiting (s), or press Enter for no limit: ")

    # Check if a value has been entered
    # sleep_time = float(sleep_time_input) if sleep_time_input else None

    # Download each URL to the specified output directory
    for url in urls:
        download_file(url, output_dir)
        # if sleep_time is not None:
        #     time.sleep(sleep_time)

def main():
    # dates = '10242023'
    input_filename = 'urls.txt'
    parent_dir = f"C:\\path\\to\\folder\\"
    output_dir = f"C:\\path\\to\\folder\\"
    process_file(input_filename, parent_dir, output_dir)

# This block checks if the script is being executed directly or being imported
if __name__ == "__main__":
    main()
