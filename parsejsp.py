import re

with open('info.jsp', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract <body> content
body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
if body_match:
    body_content = body_match.group(1).strip()

    # Extract specific values using regex
    name_match = re.search(r'Name:\s*(\w+)', body_content)
    commitid_match = re.search(r'commitid:\s*(\w+)', body_content)
    startuptime_match = re.search(r'startuptime:\s*([\d-]+)', body_content)

    print("Extracted Info:")
    if name_match:
        print("Name:", name_match.group(1))
    if commitid_match:
        print("Commit ID:", commitid_match.group(1))
    if startuptime_match:
        print("Startup Time:", startuptime_match.group(1))
