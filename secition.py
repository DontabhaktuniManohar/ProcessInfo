def read_sectioned_file(file_path):
    sections = {}
    current_section = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                # New section found
                current_section = line[1:-1]  # Extract section name without brackets
                sections[current_section] = []
            elif current_section and line:
                # Add line to the current section
                sections[current_section].append(line)

    return sections

# Example usage
file_path = "data.txt"  # Path to your file
data = read_sectioned_file(file_path)
for section, lines in data.items():
    print(f"Section [{section}]:")
    for line in lines:
        print(f"  - {line}")
