import os
from hashlib import md5
from collections import defaultdict

# Set the path to your Google Drive folder in WSL format
GOOGLE_DRIVE_PATH = '/mnt/g/My Drive/'

# Function to calculate the MD5 hash of a file
def hash_file(file_path):
    if not os.path.isfile(file_path):
        return None
    with open(file_path, 'rb') as f:
        file_hash = md5(f.read()).hexdigest()
    return file_hash

# Get a list of all files in your Google Drive folder
files = []
for root, dirs, filenames in os.walk(GOOGLE_DRIVE_PATH):
    for filename in filenames:
        file_path = os.path.join(root, filename)
        file_size = os.path.getsize(file_path)
        # Skip zero-size files
        if file_size == 0:
            continue
        file = {
            'name': filename,
            'path': file_path,
            'size': file_size
        }
        files.append(file)

# Group files by their MD5 hash
file_groups = defaultdict(list)
for file in files:
    file_hash = hash_file(file['path'])
    if file_hash is not None:
        file_groups[file_hash].append(file)

# Print out any groups with more than one file
for file_hash, file_group in file_groups.items():
    if len(file_group) > 1:
        print(f'Duplicate files with hash value {file_hash}:')
        for file in file_group:
            print(f"{file['path']}")
        print('')
