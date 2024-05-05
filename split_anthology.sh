#!/bin/bash

# Function to check if file exists
file_exists() {
    if [ -f "$1" ]; then
        return 0 # File exists
    else
        return 1 # File does not exist
    fi
}

# URL of the file to download
url="https://aclanthology.org/anthology.bib.gz"

# File name
file_name="anthology.bib.gz"

# Check if the file already exists
if file_exists "$file_name"; then
    echo "File $file_name already exists. Skipping download."
else
    # Download the file if it doesn't exist
    wget "$url"

    # Check if download was successful
    if [ $? -eq 0 ]; then
        echo "Download successful."
    else
        echo "Download failed. Exiting."
        exit 1
    fi
fi

# Decompress the file
gzip -d "$file_name"

# Check if decompression was successful
if [ $? -eq 0 ]; then
    echo "Decompression successful."
else
    echo "Decompression failed. Exiting."
    exit 1
fi

# Split the anthology.bib file into multiple files with a max size of 50 MB
python3 split.py

# Check if splitting was successful
if [ $? -eq 0 ]; then
    echo "Splitting successful."
else
    echo "Splitting failed. Exiting."
    exit 1
fi