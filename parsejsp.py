from bs4 import BeautifulSoup

# Read the JSP file
with open('info.jsp', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse it like HTML
soup = BeautifulSoup(content, 'html.parser')

# Example: extract all text
print(soup.get_text())

# Example: extract all <title> tags
title = soup.title.string
print("Title:", title)
