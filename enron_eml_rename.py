import os
import sys

# Get all files in directory
rootDirs = os.listdir(sys.argv[1])
# Iterate over all files in directory
for folder in rootDirs:
    userDirs = os.listdir(f'{sys.argv[1]}/{folder}')
    for userDir in userDirs:
        path = f'{sys.argv[1]}/{folder}/{userDir}'
        if os.path.isdir(path) :
            files = os.listdir(path)
            for file in files:
                directory = f'{sys.argv[1]}/{folder}/{userDir}'
                # Change extension of file to .eml
                os.rename(f'{directory}/{file}', f'{directory}/{file}.eml')