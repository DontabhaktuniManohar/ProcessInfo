#!/bin/bash

# Variables
DIRECTORY="/path/to/your/directory"
NEW_FILE="file-y.y.y.jar"
BACKUP_SUFFIX=".bak"

# Identify the file to backup
OLD_FILE=$(ls $DIRECTORY | grep -E "file-[0-9]+\.[0-9]+\.[0-9]+\.jar")

# Check if the old file exists
if [ -z "$OLD_FILE" ]; then
  echo "No matching file found to backup."
  exit 1
fi

# Backup the old file
echo "Backing up $OLD_FILE..."
cp "$DIRECTORY/$OLD_FILE" "$DIRECTORY/$OLD_FILE$BACKUP_SUFFIX"

# Replace the old file with the new one
echo "Replacing $OLD_FILE with $NEW_FILE..."
cp "$DIRECTORY/$NEW_FILE" "$DIRECTORY/$OLD_FILE"

echo "Backup and replacement completed."
