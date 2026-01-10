import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# from google.colab import auth  # Commented out for non-Colab environment
# from google.cloud import bigquery  # Commented out if not needed

# Function to scrape greenlist website
def scrape_website_green(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    names = []
    # Find all text content and search for "Subject:"
    # A more robust approach is to find elements containing the text "Subject:" and extract the following text.
    for strong_tag in soup.find_all('strong'):
        if "Subject:" in strong_tag.get_text():
            # Extract the text after "Subject:" within the same element or the next sibling
            text_after_subject = strong_tag.get_text().split("Subject:", 1)[1].strip()
            names.append(text_after_subject)

    # Additionally, check for "Subject:" in other elements like 'p' tags as observed previously.
    for p_tag in soup.find_all('p'):
        text = p_tag.get_text()
        start_index = 0
        while True:
            start_index = text.find("Subject:", start_index)
            if start_index == -1:
                break
            # Extract the name after "subject:"
            name_start = start_index + len("Subject:")
            # Find the end of the name (assuming it ends with a newline or the end of the text)
            name_end = text.find('\n', name_start)
            if name_end == -1:
                name = text[name_start:].strip()
            else:
                name = text[name_start:name_end].strip()
            if name and name not in names:  # Only add non-empty and unique names
                names.append(name)
            start_index = name_start + len("Subject:")  # Continue searching from after the found subject

    return names

# Scrape greenlist
url_green = "https://greenlist.tokyojon.com/"
names_list_green = scrape_website_green(url_green)
df_names_green = pd.DataFrame(names_list_green, columns=['Subject Name'])

# Save the DataFrame to a CSV file
df_names_green.to_csv('../data/greenlist.csv', index=False)

print("Greenlist names:")
print(df_names_green.head(10))

# Function to scrape blacklist website
def scrape_website_black(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    names = set()  # Use a set to store unique names efficiently

    # Search for "Subject:" in various common text-holding tags
    tags_to_check = ['p', 'div', 'span', 'li', 'td', 'strong']

    for tag_name in tags_to_check:
        for tag in soup.find_all(tag_name):
            text = tag.get_text()
            # Use regex to find all occurrences of "Subject:" followed by text
            # This regex looks for "Subject:", then captures any characters non-greedily
            # until a newline, another "Subject:", or the end of the string.
            # It also handles potential spaces after "Subject:".
            for match in re.finditer(r"Subject:\s*(.*?)(?=\nSubject:|\n|$)", text, re.IGNORECASE | re.DOTALL):
                name = match.group(1).strip()
                if name:
                    # Take the first line if there are multiple lines (e.g., name followed by comments on new line)
                    name = name.split('\n')[0].strip()
                    if name:
                        names.add(name)

    return sorted(list(names))

# Scrape blacklist
url_black = "https://blacklist.tokyojon.com/"
names_list_black = scrape_website_black(url_black)
df_names_black = pd.DataFrame(names_list_black, columns=['Subject Name'])

# Save the DataFrame to a CSV file
df_names_black.to_csv('../data/blacklist.csv', index=False)

print(f"Total names extracted from blacklist: {len(names_list_black)}")
print("Blacklist names:")
print(df_names_black.head(20))