import os
import re
from collections import defaultdict
from datetime import datetime

# Function to pad the increment number
def pad_number(number, padding):
    return str(number).zfill(padding)

# Main function to rename files
def process_filenames(directory_path):
    # Regular expression patterns to match the files
    video_pattern = re.compile(r'(2023-\d{2}-\d{2})_([A-Z0-9]+)-.*main\.mp4')
    overlay_pattern = re.compile(r'(2023-\d{2}-\d{2})_([A-Z0-9]+)-.*overlay\.png')
    image_pattern = re.compile(r'(2023-\d{2}-\d{2})_([A-Z0-9]+)-.*main\.jpg')

    # Dictionary to keep track of the incrementing numbers and filenames for each day
    increment_dict = defaultdict(lambda: defaultdict(int))
    filename_dict = defaultdict(lambda: defaultdict(dict))
    
    # List to store filenames and modification times
    video_files = []

    # First pass to rename videos and images and to populate filename_dict
    for filename in os.listdir(directory_path):
        if video_match := video_pattern.match(filename):
            # Get the last modified time of the file
            file_path = os.path.join(directory_path, filename)
            modification_time = os.path.getmtime(file_path)
            video_files.append((filename, modification_time))
        elif image_match := image_pattern.match(filename):
            date, uid = image_match.groups()
            increment_dict[date]['image'] += 1
            increment_number = pad_number(increment_dict[date]['image'], 3)
            new_filename = f"{date}-image-{increment_number}_{uid}.jpg"
            filename_dict[date][uid]['image'] = increment_number
            old_file = os.path.join(directory_path, filename)
            new_file = os.path.join(directory_path, new_filename)
            os.rename(old_file, new_file)
            print(f'Renamed "{filename}" to "{new_filename}"')

    # Sort the video files by modification time in ascending order
    video_files.sort(key=lambda x: x[1], reverse=True)
    for filename, _ in video_files:
        video_match = video_pattern.match(filename)
        if video_match:
            date, uid = video_match.groups()
            increment_dict[date]['video'] += 1
            increment_number = pad_number(increment_dict[date]['video'], 3)
            new_filename = f"{date}-video-{increment_number}_{uid}.mp4"
            filename_dict[date][uid]['video'] = increment_number
            old_file = os.path.join(directory_path, filename)
            new_file = os.path.join(directory_path, new_filename)
            os.rename(old_file, new_file)
            print(f'Renamed "{filename}" to "{new_filename}"')

    # Second pass to rename overlay files based on the populated filename_dict
    for filename in os.listdir(directory_path):
        if overlay_match := overlay_pattern.match(filename):
            date, uid = overlay_match.groups()
            for media_type in ['video', 'image']:
                if uid in filename_dict[date] and media_type in filename_dict[date][uid]:
                    increment_number = filename_dict[date][uid][media_type]
                    new_filename = f"{date}-{media_type}-{increment_number}-overlay_{uid}.png"
                    old_file = os.path.join(directory_path, filename)
                    new_file = os.path.join(directory_path, new_filename)
                    os.rename(old_file, new_file)
                    print(f'Renamed "{filename}" to "{new_filename}"')
                    break

def main():
    directory_path = 'H:\\SnapChat Data & Memories Download\\New\\Extracted\\test\\'
    process_filenames(directory_path)

# Call the main function with the directory path
if __name__ == "__main__":
    main()