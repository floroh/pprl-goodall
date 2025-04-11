#!/bin/bash

# Variables
NEXTCLOUD_URL="https://cloud.scadsai.uni-leipzig.de/index.php/s/YcLwFaqYgejiC9c/download/datasets-sigmod2025-pprl.zip"  # Replace with your Nextcloud shared link
OUTPUT_ZIP="datasets.zip"  # Name of the output zip file
EXTRACT_DIR="datasets"  # Directory to extract files into

# Download the ZIP file
echo "Downloading ZIP file..."
curl -L -o "$OUTPUT_ZIP" "$NEXTCLOUD_URL"

# Check if the download was successful
if [ $? -ne 0 ]; then
    echo "Error downloading the file."
    exit 1
fi

# Create a directory for extraction
mkdir -p "$EXTRACT_DIR"

# Extract the ZIP file
echo "Extracting ZIP file..."
unzip -o "$OUTPUT_ZIP" -d "$EXTRACT_DIR"

# Check if the extraction was successful
if [ $? -ne 0 ]; then
    echo "Error extracting the ZIP file."
    exit 1
fi

echo "Download and extraction completed successfully."
