# Define the file paths
input_file = 'input.txt'
output_file = 'output.txt'

# Step 1: Read the content of the file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Step 2: Sort the content
sorted_lines = sorted(lines)

# Step 3: Write the sorted content back to a new file (optional)
with open(output_file, 'w') as file:
    file.writelines(sorted_lines)

print("File sorted and saved as output.txt")
