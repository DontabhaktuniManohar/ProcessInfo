#!/bin/bash

# Specify the file path
FILE_PATH="your_file.properties"

# Check if the file exists
if [[ -f "$FILE_PATH" ]]; then
    # Check if 'jvmd_count' exists in the file
    if ! grep -q "^jvmd_count=" "$FILE_PATH"; then
        # Add 'jvmd_count=1' to the file
        echo "jvmd_count=1" >> "$FILE_PATH"
        echo "Added 'jvmd_count=1' to the file."
    else
        echo "'jvmd_count' already exists in the file."
    fi
else
    echo "File not found: $FILE_PATH"
fi
