import os
import sys

# Get all files in directory
files = os.listdir(sys.argv[1])
# Iterate over all files in directory
for file in files:
    # Change extension of file to .eml
    os.rename(f'{sys.argv[1]}{file}', f'{sys.argv[1]}{file}.eml')
